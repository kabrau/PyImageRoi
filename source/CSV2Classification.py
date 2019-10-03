import os
import io
import pandas as pd
import tensorflow as tf
import argparse
import cv2

from PIL import Image
from object_detection.utils import dataset_util
from collections import namedtuple, OrderedDict

#python CSV2Classification.py  
# --csv_input=E:/GitHub/DA-Faster-RCNN/Kitti-pseudo-Cityscape-5-5/pseudolabel-0.5.csv  
# --output_path=E:/GitHub/DA-Faster-RCNN/Kitti-pseudo-Cityscape-5-5/class_images/

#----------------------------------------------------------------------------------------
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--csv_input", required=True, help="Path to the CSV input")
ap.add_argument("-o", "--output_path", required=True, help="Path to output images")
ap.add_argument("-i", "--images_path", required=False, help="Path for Images, If dont have into CSV")

args = vars(ap.parse_args())

def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]


def saveFiles(group, path, output_path):
    if path==None:
        path = group.filename[1]
        filename = group.filename[0]
    else:
        filename = group.filename

    imageFile = os.path.join(path, '{}'.format(filename))
    if not os.path.isfile(imageFile):
        raise Exception("File not found: "+imageFile)

    image = cv2.imread(imageFile) 
    # with tf.gfile.GFile(imageFile, 'rb') as fid:
    #     encoded_jpg = fid.read()
    # encoded_jpg_io = io.BytesIO(encoded_jpg)
    # image = Image.open(encoded_jpg_io)
    # width, height = image.size

    # filename = group.filename[0].encode('utf8')
    # image_format = b'jpg'
    # xmins = []
    # xmaxs = []
    # ymins = []
    # ymaxs = []
    # classes_text = []
    # classes = []

    i = 0
    for index, row in group.object.iterrows():
        xmin = min(row['xmin'],row['xmax'])
        xmax = max(row['xmin'],row['xmax'])
        ymin = min(row['ymin'],row['ymax'])
        ymax = max(row['ymin'],row['ymax'])

        fileSplit = filename.split('.')
        outFile = os.path.join(output_path,fileSplit[0]+"-"+str(i)+"."+fileSplit[1])
        i = i+1

        print(outFile,xmin,ymin,xmax,ymax)
        classImage = image[ymin:ymax,xmin:xmax]
        cv2.imwrite(outFile, classImage)

        # xmins.append(row['xmin'] / width)
        # xmaxs.append(row['xmax'] / width)
        # ymins.append(row['ymin'] / height)
        # ymaxs.append(row['ymax'] / height)
        # classes_text.append(row['class'].encode('utf8'))
        # classes.append(class_text_to_int(row['class']))

    # tf_example = tf.train.Example(features=tf.train.Features(feature={
    #     'image/height': dataset_util.int64_feature(height),
    #     'image/width': dataset_util.int64_feature(width),
    #     'image/filename': dataset_util.bytes_feature(filename),
    #     'image/source_id': dataset_util.bytes_feature(filename),
    #     'image/encoded': dataset_util.bytes_feature(encoded_jpg),
    #     'image/format': dataset_util.bytes_feature(image_format),
    #     'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
    #     'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
    #     'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
    #     'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
    #     'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
    #     'image/object/class/label': dataset_util.int64_list_feature(classes),
    # }))
    return #tf_example

def main(_):
    
    output_path = args["output_path"]
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    path = args["images_path"]

    examples = pd.read_csv(args["csv_input"])
    if path==None:
        grouped = split(examples, ['filename','path'])
    else:
        grouped = split(examples, ['filename'])

    for group in grouped:

        print(group.filename[0])
        saveFiles(group, path, output_path)

    
    print('Successfully ')






#----------------------------------------------------------------------------------------
if __name__ == '__main__':
    tf.app.run()