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

TEST_PATH =  "E:/Datasets/pedestrianlights-5971774/test/"
#TEST_PATH = os.path.join(datasetpath,"groundtruth_large.txt")

label_map = label_map_util.load_labelmap("C:/Users/marcelo/Google Drive/Doutorado/WCCI2018/5971774/config/signal_map_3C.pbtxt")
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=1, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

models_base_path = "C:/Users/marcelo/Google Drive/Doutorado/WCCI2018/5971774/frozen"
models_path = os.listdir(models_base_path)
#print(models_path)
models_path.sort(key=natural_keys)

#with open(TEST_PATH, "rb") as f:
#    test_files = f.read().splitlines()

models_path = ['AAA']
for model_path in models_path:
  tf.reset_default_graph()
  #print (model_path)
  #PATH_TO_CKPT = os.path.join(models_base_path, model_path, "frozen_inference_graph.pb")
  PATH_TO_CKPT = os.path.join(models_base_path, "frozen_inference_graph.pb")

  detection_graph = tf.Graph()
  with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
      serialized_graph = fid.read()
      od_graph_def.ParseFromString(serialized_graph)
      tf.import_graph_def(od_graph_def, name='')

  dest_path = os.path.join(models_base_path, "results_pedestrianlights_large/")
  if not os.path.exists(dest_path + model_path):
      os.makedirs(dest_path + model_path)

  outfiles = []
  # outfiles += [open(dest_path + model_path+"/signal.txt","w")]
  outfiles += [open(dest_path + model_path+"/go.txt","w")]
  outfiles += [open(dest_path + model_path+"/stop.txt","w")]
  outfiles += [open(dest_path + model_path+"/off.txt","w")]
  
  print("=======================================================")
  print(outfiles)
  print("=======================================================")

  plot_results = False
  show_time = False

  test_files = os.listdir("E:/Datasets/pedestrianlights-5971774/test") 

  with detection_graph.as_default():
      with tf.Session(graph=detection_graph) as sess:
          for image_path in test_files:
              #print ( os.path.join(TEST_PATH, image_path)) 
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
              
              
              # Visualization of the results of a detection.
              vis_util.print_bounding_box_on_log(
                  image_path.split("/")[-1], 
                  # image_path[len(image_path[:image_path[:image_path.rfind("/")].rfind("/")])+1:],
                  image_np, 
                  np.squeeze(boxes),
                  np.squeeze(classes).astype(np.int32),
                  np.squeeze(scores),
                  outfiles,
                  threshold=0.01
              )
              
              if show_time:
                print (time.time() - t  )            
              
              if plot_results:
                  vis_util.visualize_boxes_and_labels_on_image_array(
                    image_np,
                    np.squeeze(boxes),
                    np.squeeze(classes).astype(np.int32),
                    np.squeeze(scores),
                    category_index,
                    use_normalized_coordinates=True,
                    line_thickness=8)
                  plt.figure(figsize=IMAGE_SIZE)
                  plt.imshow(image_np)
              
  for log_file in outfiles:
      log_file.close()