#!/usr/bin/env python
import re
import argparse
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import xml.etree.ElementTree as ET
import os
from collections import defaultdict
import sys
from itertools import cycle
from sklearn.metrics import auc
from argparse import RawTextHelpFormatter

classes = ["butt","breast","frontalm","frontalf"]

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)', text) ]

class bcolors:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   ENDC = '\033[0m'

class Box():
    def __init__(self):
        self.cls = None
        self.score = None
        self.x = 0
        self.y = 0
        self.xx = 0
        self.yy = 0
        self.w = 0
        self.h = 0

    def set_WH(self):
        self.w = self.xx - self.x
        self.h = self.yy - self.y

    def load_from_line(self, line, class_name):

        #print(line)
        
        #macgyver for file name with spaces
        spaceCount = line.count(' ')
        if spaceCount > 5:
            line = line.replace(' ','▼', spaceCount-5 )
            #print(spaceCount , line.count(' '))
            data = line.split(" ")
            data[0] = data[0].replace('▼',' ')
        else:
            data = line.split(" ")


        self.score = float(data[1])
        self.cls = class_name
        self.x = int(round(float(data[2])))
        self.y = int(round(float(data[3])))
        self.xx = int(round(float(data[4])))
        self.yy = int(round(float(data[5])))
        self.set_WH()

    def __str__(self):
        if self.score == None:
            return "X:{} Y:{} XX:{} YY:{} W:{} H:{} Class:{}".format(self.x,self.y,self.xx,self.yy, self.w, self.h, self.cls)
        else:
            return "X:{} Y:{} XX:{} YY:{} W:{} H:{} Class:{} Score:{}".format(self.x,self.y,self.xx,self.yy, self.w, self.h, self.cls, self.score)

def auc_(pv,rv):
    r = 0.0
    for p,v in zip(pv,rv):
        r += (abs(p) + abs(v)) - 1.0
    return r / float(len(pv))

def overlap(x1, w1, x2, w2):
    l1 = x1 - (w1 / 2.0)
    l2 = x2 - (w2 / 2.0)
    left = l1 if l1 > l2 else l2
    r1 = x1 + (w1 / 2.0)
    r2 = x2 + (w2 / 2.0)
    right = r1 if r1 < r2 else r2
    return right - left

def box_intersection(a, b):
    w = overlap(a.x, a.w, b.x, b.w)
    h = overlap(a.y, a.h, b.y, b.h)
    if w < 0 or h < 0: return 0
    area = w * h
    return area

def box_union(a, b):
    i = box_intersection(a, b)
    u = a.w * a.h + b.w * b.h - i
    return u

def box_iou(a, b):
    if box_union(a, b) == 0:
        return 0.0
    return box_intersection(a, b) / box_union(a, b)

def get_truth_boxes(path, class_name):
    in_file = open(path, "r")
    tree = ET.parse(in_file)
    root = tree.getroot()    
    has_boxes = False
    boxes = []

    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls != class_name:
            continue

        b = obj.find('bndbox')
        box = Box()
        box.cls = cls
        box.x = int(b.find('xmin').text)
        box.y = int(b.find('ymin').text)
        box.xx = int(b.find('xmax').text)
        box.yy = int(b.find('ymax').text)
        box.set_WH()
        boxes += [box]

    return boxes

def precision(tp, fp):
    if tp + fp == 0:
        return 0.0
    return tp/float(tp + fp)

def recall(tp, fn):
    if tp + fn == 0:
        return 0.0
    return tp/float(tp + fn)

def f_measure(precision, recall):
    if precision + recall == 0.0:
        return 0.0
    return 2.0 * ((precision * recall) / (precision + recall))

def voc_ap(rec, prec):
    # correct AP calculation
    # first append sentinel values at the end
    mrec = np.concatenate(([0.], rec, [1.]))
    mpre = np.concatenate(([0.], prec, [0.]))

    # compute the precision envelope
    for i in range(mpre.size - 1, 0, -1):
        mpre[i - 1] = np.maximum(mpre[i - 1], mpre[i])

    # to calculate area under PR curve, look for points
    # where X axis (recall) changes value
    i = np.where(mrec[1:] != mrec[:-1])[0]

    # and sum (\Delta recall) * prec
    ap = np.sum((mrec[i + 1] - mrec[i]) * mpre[i + 1])
    return ap


def run(LABELS_PATH, results_path, classes, IOU_THRESH, scoreInitial, verbose):

    best_precision = 0
    best_recall = 0
    best_f = 0
    best_p_threshold = 0
    best_r_threshold = 0
    best_f_threshold = 0
    best_t_thres_values = []
    
    results_list = os.listdir(results_path)
    results_list.sort(key=natural_keys)

    for results in results_list:
        recall_values = defaultdict(list)
        precision_values = defaultdict(list)
        print()
        print('========= ',results,' ===========')
        
        results_chart_path = os.path.join(results_path, results,"_chart")
        print( 'Chart path : ', results_chart_path)
        if not os.path.exists(results_chart_path):
            os.makedirs(results_chart_path)

        for CLASS in classes:                    
            
            print( "class ->", os.path.join(results_path, results, CLASS+".txt"))
            PREDICTIONS_PATH = os.path.join(results_path, results, CLASS+".txt")

            SCORE_THRESH = scoreInitial            

            predictions_dict = defaultdict(list)
            truth_dict       = defaultdict(list)

            with open(PREDICTIONS_PATH, "r") as f:
                predictions_lines = f.read().splitlines()

            for line in predictions_lines:
                b = Box()
                b.load_from_line(line, CLASS)

                #macgyver for file name with spaces
                spaceCount = line.count(' ')
                if spaceCount > 5:
                    line = line.replace(' ','▼', spaceCount-5 )
                    img_name = line.split(" ")[0].replace('▼',' ')
                else:
                    img_name = line.split(" ")[0]

                
                predictions_dict[img_name] += [b]

                if img_name not in truth_dict:
                    label_file_name = img_name
                    # if "tumblr" in img_name:
                    #     label_file_name += ".gif"
                    truth_dict[img_name] += get_truth_boxes(os.path.join(LABELS_PATH, label_file_name + ".xml"), CLASS)
            
            best_f = -1.0
            best_result = None
            while SCORE_THRESH <= 0.95:
                tp = 0
                fp = 0
                fn = 0
                sc = 0     

                for pred_key,predicted_boxes in predictions_dict.items(): #.iteritems():
                    truth_boxes = list(truth_dict[pred_key])
                    predicted_boxes = list(predicted_boxes)

                    truth_detected = []
                    pred_detected = []
                    for truth_box in truth_boxes:
                        if truth_box in truth_detected: continue
                        max_iou = -1.0
                        detected_truth_box = None
                        detected_pred_box = None
                        for pred_box in predicted_boxes:
                            if pred_box in pred_detected: continue
                            if pred_box.score < SCORE_THRESH:
                                continue

                            if box_iou(pred_box, truth_box) > max_iou:
                                max_iou = box_iou(pred_box, truth_box)
                                detected_truth_box = truth_box
                                detected_pred_box  = pred_box

                        if max_iou >= IOU_THRESH:
                            truth_detected += [detected_truth_box]
                            pred_detected += [detected_pred_box]

                    fn += len(truth_boxes) - len(truth_detected)
                    tp += len(truth_detected)
                    fp += len([b for b in predicted_boxes if b.score >= SCORE_THRESH]) - len(pred_detected)

                precision_values[CLASS] += [precision(tp, fp)]
                recall_values[CLASS] += [recall(tp, fn)]

                if recall(tp, fn) < 0.01:
                    break

                result =  "TP:{} FP:{} FN:{} Precision:{} Recall:{} F:{} Score Threshold:{}".format(tp, fp, fn, precision(tp, fp), recall(tp, fn), f_measure(precision(tp, fp), recall(tp, fn)), SCORE_THRESH)            
                if verbose:
                    print( result)

                if precision(tp, fp) > best_precision:
                    best_precision = precision(tp, fp)
                    best_p_threshold = SCORE_THRESH

                if recall(tp, fn) > best_recall:
                    best_recall = recall(tp, fn)
                    best_r_threshold = SCORE_THRESH

                if f_measure(precision(tp, fp), recall(tp, fn)) > best_f:
                    best_f = f_measure(precision(tp, fp), recall(tp, fn))
                    best_f_threshold = SCORE_THRESH

                SCORE_THRESH += 0.01
            print( "PRECISION", CLASS, best_precision, best_p_threshold)
            print( "RECALL", CLASS, best_recall, best_r_threshold                        )
            print( "F", CLASS, best_f, best_f_threshold)
            best_t_thres_values += [best_f_threshold]                     

            colors = cycle(['red', 'gold', 'aqua', 'magenta'])

        f = plt.figure()
        ax = plt.subplot(111)

        for c, color in zip(classes, colors):
            precision_values[c] = np.concatenate(([0.], precision_values[c], [1.]))
            recall_values[c] = np.concatenate(([1.], recall_values[c], [0.]))
            line,= ax.plot(recall_values[c], precision_values[c], '+-', color=color, label='{0} AP={1:0.2f}'.format(c, voc_ap(np.flip(recall_values[c][1:-1],0), np.flip(precision_values[c][1:-1],0))))

        plt.xlim([-0.02, 1.02])
        plt.ylim([-0.02, 1.02])
        plt.ylabel('Precision')

        ax.set_xlabel('Recall')    
        ax.xaxis.set_label_position('top') 
        ax.xaxis.tick_top()

        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height * 0.1,
                         box.width, box.height * 0.9])

        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
              fancybox=True, shadow=True, ncol=2)
        ax.grid(True)

        ticklines = ax.get_xticklines() + ax.get_yticklines()
        gridlines = ax.get_xgridlines() + ax.get_ygridlines()
        ticklabels = ax.get_xticklabels() + ax.get_yticklabels()

        for line in ticklines:
            line.set_linewidth(3)

        for line in gridlines:
            line.set_linestyle('-.')
            line.set_color('gray')

        f.savefig(os.path.join(results_chart_path,"chart.pdf"))                
        plt.close("all")

        print('---- mAPs of ',results,'---')
        values = 0.0
        for classe in classes:
            print(classe, voc_ap(np.flip(recall_values[classe][1:-1],0), np.flip(precision_values[classe][1:-1],0)))
            values += voc_ap(np.flip(recall_values[classe][1:-1],0), np.flip(precision_values[classe][1:-1],0))
        print("mAP:", values / float(len(classes)))
        sys.stdout.flush()
    #print(len(best_t_thres_values))
    #print( np.average(np.asarray(best_t_thres_values)))

if __name__ == "__main__":

    #=============================================================================
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser(description="TOOL to calc mAP\n"+
                                 "More information on: "+
                                 "https://github.com/kabrau/PyImageRoi", 
                                 formatter_class=RawTextHelpFormatter)

    ap.add_argument("-a", "--annpath", required=True, help="Pascal VOC annotation path")
    ap.add_argument("-r", "--resultpath", required=True, help="Path of method results")
    ap.add_argument("-c", '--class', required=True, nargs='*', help='list of class, e.g. --classes dog cat mouse')
    ap.add_argument("-i", '--IOU', required=True, type=float, help='IOU confidence threshold, e.g. 0.5')
    ap.add_argument("-v", "--verbose", nargs='?', type=bool, default=False, required=False, help="show verbose")

    args = vars(ap.parse_args())

    run(args["annpath"], args["resultpath"], args["class"], args["IOU"], 0.0, (args["verbose"] is None))

# python mAP.py -a E:\Datasets\signal\test.ann.GoStop -r E:\GitHub\PedestrialTrafficLight\accurace_calc\results\3C\ -c go stop off -i 0.5