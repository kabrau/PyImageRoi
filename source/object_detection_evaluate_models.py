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


def run(TEST_PATH, LABEL_MAP, PATH_TO_CKPT, DEST_PATH):
  


    #TEST_PATH =  "F:/datasets/Cityscape/val/"
    #LABEL_MAP = "F:/datasets/Cityscape/cityscape_label_map.pbtxt"
    #PATH_TO_CKPT = "F:/datasets/Cityscape/inference/frozen_inference_graph.pb"
    #DEST_PATH = "F:/datasets/Cityscape/result"

  
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


  f_out = []
  for c in categories:
    #print(c['name'], category_index, categories)
    f_out.append(open(dest_path +"/"+c['name']+".txt","w"))


  plot_results = False
  show_time = False

  valid_images = [".jpg",".gif",".png",".tga",".jpeg"]

  test_files = os.listdir(TEST_PATH) 
  with detection_graph.as_default():
      with tf.Session(graph=detection_graph) as sess:
          for image_path in test_files:

              name, ext = os.path.splitext(image_path)        
              if ext.lower() not in valid_images:            
                continue

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
              if show_time:
                t = time.time()

              (boxes, scores, classes, num_detections) = sess.run(
                [boxes, scores, classes, num_detections],
                feed_dict={image_tensor: image_np_expanded})

              min_score_thresh = 0.01
              

              #prediction = ""
              for i in range(boxes.shape[1]):
                #print(boxes.shape, classes.shape)
                if scores[0][i] > min_score_thresh:
                  box = tuple(boxes[0][i].tolist())
                  #print(box)
                  #print(image.shape)
                  class_name = category_index[classes[0][i]]['name']
                  #print(class_name)

                  im_width = image.shape[1]
                  im_height = image.shape[0]
                  ymin, xmin, ymax, xmax = box
                  
                  (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                  ymin * im_height, ymax * im_height)
                  #print(class_name, scores[0][i], left, right, top, bottom)
                  #prediction = prediction + class_name +" "+str(scores[0][i])+" "+ str(int(left))+" "+ str(int(right))+" "+ str(int(top))+" "+ str(int(bottom))+"\n"
                  #print(classes[0][i], image_path+" "+str(scores[0][i])+" "+ str(int(left))+" "+ str(int(right))+" "+ str(int(top))+" "+ str(int(bottom))+"\n")
                  #f_out[int(classes[0][i]-1)].write(image_path+" "+str(scores[0][i])+" "+ str(int(left))+" "+ str(int(right))+" "+ str(int(top))+" "+ str(int(bottom))+"\n")
                  f_out[int(classes[0][i]-1)].write(image_path+" "+str(scores[0][i])+" "+ str(left)+" "+ str(top)+" "+ str(right)+" "+ str(bottom)+"\n")

                  #image_pil = Image.fromarray(np.uint8(image)).convert('RGB')
                  #im_width, im_height = image_pil.size
                  #(left, right, top, bottom) = (xmin * im_width, xmax * im_width, ymin * im_height, ymax * im_height)
                  #print(left, right, top, bottom)
              
              #filename, file_extension = os.path.splitext(image_path)
              #dest_file = dest_path + filename + ".txt"
              #print(dest_file
              #f= open(dest_file,"w+")
              #f.write(prediction)
              #f.close()
              

              #sys.exit()            

              #print(boxes, scores, classes, num_detections)
                
              
              
              
              # Visualization of the results of a detection.
              # vis_util.print_bounding_box_on_log(
              #     image_path.split("/")[-1], 
              #     # image_path[len(image_path[:image_path[:image_path.rfind("/")].rfind("/")])+1:],
              #     image_np, 
              #     np.squeeze(boxes),
              #     np.squeeze(classes).astype(np.int32),
              #     np.squeeze(scores),
              #     outfiles,
              #     threshold=0.01
              # )
              
              if show_time:
                print (time.time() - t  )            
              
              # if plot_results:
              #     vis_util.visualize_boxes_and_labels_on_image_array(
              #       image_np,
              #       np.squeeze(boxes),
              #       np.squeeze(classes).astype(np.int32),
              #       np.squeeze(scores),
              #       category_index,
              #       use_normalized_coordinates=True,
              #       line_thickness=8)
              #     #plt.figure(figsize=IMAGE_SIZE)
              #     #plt.imshow(image_np)
              #     #plt.show()
              #     cv2.imwrite("c:/tempo/z.png",image_np)
              
  #for log_file in outfiles:
  #    log_file.close()
  for f in f_out:
    f.close()


if __name__ == "__main__":

    

    #=============================================================================
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()

    ap.add_argument("-i", "--imagepath", required=True, help="")
    ap.add_argument("-l", "--labelpath", required=True, help="")
    ap.add_argument("-f", "--frozenfile", required=True, help="")
    ap.add_argument("-o", "--output", required=True, help="")
    

    args = vars(ap.parse_args())

    #TEST_PATH =  "F:/datasets/Cityscape/val/"
    #LABEL_MAP = "F:/datasets/Cityscape/cityscape_label_map.pbtxt"
    #PATH_TO_CKPT = "F:/datasets/Cityscape/inference/frozen_inference_graph.pb"
    #DEST_PATH = "F:/datasets/Cityscape/result"

    

    run(args["imagepath"], args["labelpath"], args["frozenfile"], args["output"])