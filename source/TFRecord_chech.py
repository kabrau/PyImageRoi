import tensorflow as tf
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--TFfile", required=True, help="TFRecord file")

args = vars(ap.parse_args())

#for example in tf.python_io.tf_record_iterator(args["TFfile"]):
#    result = tf.train.Example.FromString(example)

# reader = tf.TFRecordReader()
# _, serialized_example = reader.read(args["TFfile"])
# features = tf.parse_single_example(
#   serialized_example,
#   # Defaults are not specified since both keys are required.
#   features={
#       'image_raw': tf.FixedLenFeature([], tf.string),
#       'label': tf.FixedLenFeature([], tf.int64),
#       'height': tf.FixedLenFeature([], tf.int64),
#       'width': tf.FixedLenFeature([], tf.int64),
#       'depth': tf.FixedLenFeature([], tf.int64)
#   })

def load_tfrecord(file_name):
    features = {'x': tf.FixedLenFeature([2], tf.int64)}
    data = []
    tot = 0
    for s_example in tf.python_io.tf_record_iterator(file_name):
        example = tf.parse_single_example(s_example, features=features)
        result = tf.train.Example.FromString(s_example)
        print("filename={}".format(result.features.feature['image/filename'].bytes_list.value))
        print(result.features.feature['image/format'].bytes_list.value)
        print(len(result.features.feature['image/encoded'].bytes_list.value[0]))
        
        #print(tf.expand_dims(example['x'], 0))
        data.append(tf.expand_dims(example['x'], 0))
        tot += 1
        #break
    print("Total={}".format(tot))
    #return tf.concat(0, data)

data = load_tfrecord(args["TFfile"])