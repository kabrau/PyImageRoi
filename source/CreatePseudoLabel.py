#!/usr/bin/env python
import numpy as np
import os
import six.moves.urllib as urllib
import sys
sys.path.append('E:/GitHub/TensorFlow/models/research')
sys.path.append('E:/GitHub/TensorFlow/models/research/object_detection')

import tarfile
import tensorflow as tf
import zipfile
from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
import cv2
#sys.path.append("..")
from utils import label_map_util
from utils import visualization_utils as vis_util
import re
import time
import PIL.Image as Image
import argparse

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split('(\d+)', text) ]

def load_image_into_numpy_array(image):
    (im_width, im_height) = image.shape[1], image.shape[0]
    return image.reshape((im_height, im_width, 3)).astype(np.uint8)


def run(TEST_PATH, LABEL_MAP, PATH_TO_CKPT, DEST_PATH, min_score_thresh, classes_dest, addPath):
  
  
  label_map = label_map_util.load_labelmap(LABEL_MAP)
  qtd_label = label_map_util.get_max_label_map_index(label_map)  

  categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=qtd_label, use_display_name=True)
  category_index = label_map_util.create_category_index(categories)

  tf.reset_default_graph()   
  

  detection_graph = tf.Graph()
  with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
      serialized_graph = fid.read()
      od_graph_def.ParseFromString(serialized_graph)
      tf.import_graph_def(od_graph_def, name='')

  dest_path = DEST_PATH
  
  if not os.path.exists(dest_path):
      os.makedirs(dest_path)


  f_out = open(dest_path +"/pseudolabel-"+str(min_score_thresh)+".csv","w")
  if addPath:
    f_out.write("path,filename,width,height,class,xmin,ymin,xmax,ymax\n")
  else:
    f_out.write("filename,width,height,class,xmin,ymin,xmax,ymax\n")

  test_files = os.listdir(TEST_PATH) 
  with detection_graph.as_default():
      with tf.Session(graph=detection_graph) as sess:
          for image_path in test_files:

              print(image_path)
              
              image = cv2.imread(os.path.join(TEST_PATH, image_path))
              image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
              image_np = image.copy()
              # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
              image_np_expanded = np.expand_dims(image_np, axis=0)
              image_tensor = detection_graph.get_tensor_by_name("image_tensor:0")
              # Each box represents a part of the image where a particular object was detected.
              boxes = detection_graph.get_tensor_by_name("detection_boxes:0")
              # Each score represent how level of confidence for each of the objects.
              # Score is shown on the result image, together with the class label.
              scores = detection_graph.get_tensor_by_name('detection_scores:0')
              classes = detection_graph.get_tensor_by_name('detection_classes:0')
              num_detections = detection_graph.get_tensor_by_name('num_detections:0')
              # Actual detection.

              (boxes, scores, classes, num_detections) = sess.run(
                [boxes, scores, classes, num_detections],
                feed_dict={image_tensor: image_np_expanded})

              for i in range(boxes.shape[1]):
                
                if scores[0][i] > min_score_thresh:

                  box = tuple(boxes[0][i].tolist())

                  class_name = category_index[classes[0][i]]['name']

                  if class_name in classes_dest:
                    im_width = image.shape[1]
                    im_height = image.shape[0]
                    ymin, xmin, ymax, xmax = box                  
                    (left, right, top, bottom) = (xmin * im_width, xmax * im_width, ymin * im_height, ymax * im_height)
                    if addPath:
                      f_out.write(TEST_PATH+","+image_path+","+str(im_width)+","+str(im_height)+","+class_name+","+ str(int(left))+","+ str(int(top))+","+ str(int(right))+","+ str(int(bottom))+"\n")
                    else:
                      f_out.write(image_path+","+str(im_width)+","+str(im_height)+","+class_name+","+ str(int(left))+","+ str(int(top))+","+ str(int(right))+","+ str(int(bottom))+"\n")
              
  f_out.close()


if __name__ == "__main__":   

    #=============================================================================
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()

    ap.add_argument("-i", "--imagepath", required=True, help="")
    ap.add_argument("-l", "--labelpath", required=True, help="")
    ap.add_argument("-f", "--frozenfile", required=True, help="")
    ap.add_argument("-o", "--output", required=True, help="")
    ap.add_argument("-t", "--minthreshold", required=True, type=float, default=0.5, help="")
    ap.add_argument("-c", '--class', required=True, nargs='*', help='list of class, e.g. --classes dog cat mouse')
    ap.add_argument("-a", "--addPath", required=False, dest='addPath', action='store_const', const=True, default=False, help='')
    #python CreatePseudoLabel.py
    # -i=F:/datasets/Cityscape/train/
    # -l=F:/datasets/Kitti/Kitti_label_map.pbtxt 
    # -f=F:/datasets/Kitti/inference/frozen_inference_graph.pb 
    # -o=E:/GitHub/DA-Faster-RCNN/Kitti-pseudo-Cityscape-8 
    # -t=0.8 
    # -c car

    args = vars(ap.parse_args())
   
    run(args["imagepath"], args["labelpath"], args["frozenfile"], args["output"], args["minthreshold"], args["class"], args["addPath"])