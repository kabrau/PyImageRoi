"""
Usage:
  # From tensorflow/models/
  # Create train data:
  python generate_tfrecord.py --csv_input=data/train_labels.csv  --output_path=data/train.record

  # Create test data:
  python generate_tfrecord.py --csv_input=data/test_labels.csv  --output_path=data/test.record
"""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import io
import pandas as pd
import tensorflow as tf
import argparse

from PIL import Image
from object_detection.utils import dataset_util
from collections import namedtuple, OrderedDict


#----------------------------------------------------------------------------------------
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--csv_input", required=True, help="Path to the CSV input")
ap.add_argument("-o", "--output_path", required=True, help="Path to output TFRecord")
ap.add_argument("-i", "--images_path", required=False, help="Path for Images, If dont have into CSV")

args = vars(ap.parse_args())

#----------------------------------------------------------------------------------------

# TO-DO replace this with label map
def class_text_to_int(row_label):
    if row_label == 'face':
        return 1
    #elif row_label == 'stop':
    #    return 2
    #elif row_label == 'off':
    #    return 3
    #else:
    #    None


def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]


def create_tf_example(group, path):
    if path==None:
        path = group.filename[1]

    imageFile = os.path.join(path, '{}'.format(group.filename[0]))
    if not os.path.isfile(imageFile):
        raise Exception("File not found: "+imageFile)

    with tf.gfile.GFile(imageFile, 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    width, height = image.size

    filename = group.filename[0].encode('utf8')
    image_format = b'jpg'
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    for index, row in group.object.iterrows():
        xmins.append(row['xmin'] / width)
        xmaxs.append(row['xmax'] / width)
        ymins.append(row['ymin'] / height)
        ymaxs.append(row['ymax'] / height)
        classes_text.append(row['class'].encode('utf8'))
        classes.append(class_text_to_int(row['class']))

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))
    return tf_example


def main(_):
    writer = tf.python_io.TFRecordWriter(args["output_path"])
    path = args["images_path"]

    examples = pd.read_csv(args["csv_input"])
    if path==None:
        grouped = split(examples, ['filename','path'])
    else:
        grouped = split(examples, ['filename'])

    for group in grouped:
        tf_example = create_tf_example(group, path)
        writer.write(tf_example.SerializeToString())

    writer.close()
    output_path = os.path.join(os.getcwd(), args["output_path"])
    print('Successfully created the TFRecords: {}'.format(output_path))


#----------------------------------------------------------------------------------------
if __name__ == '__main__':
    print()
    print()
    print()
    print('==========================================================================')
    print('                      ATENTION                                            ')
    print()
    print('                      ATENTION                                            ')
    print()
    print()
    print('Hi body - dont forget update the function "class_text_to_int(row_label) " ')
    print()
    print('==========================================================================')
    print()
    print()
    print()

    tf.app.run()


