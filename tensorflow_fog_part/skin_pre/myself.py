# -*- coding: utf-8 -*-

# author:Lichang
import tensorflow as tf
import numpy as np
from PIL import Image
import cv2
import tensorflow as tf
import os

# classes = {'./img/nofrog','./img/hasfrog'}
#
# writer = tf.python_io.TFRecordWriter("frog.tfrecords")
# for index, name in enumerate(classes):
#     print(index)
#     class_path = name + "/"
#     for img_name in os.listdir(class_path):
#         img_path = class_path + img_name
#         img = Image.open(img_path)
#         # img = img.resize((224, 224))
#         img_raw = img.tobytes()              #将图片转化为原生bytes
#         print(index)
#         print(len(img_raw))
#         example = tf.train.Example(features=tf.train.Features(feature={
#             "label": tf.train.Feature(int64_list=tf.train.Int64List(value=[index])),
#             'img_raw': tf.train.Feature(bytes_list=tf.train.BytesList(value=[img_raw]))
#         }))
#         writer.write(example.SerializeToString())  #序列化为字符串
# writer.close()

def read_and_decode(filename):
    #根据文件名生成一个队列
    filename_queue = tf.train.string_input_producer([filename])

    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)   #返回文件名和文件
    features = tf.parse_single_example(serialized_example,
                                       features={
                                           'label': tf.FixedLenFeature([], tf.int64),
                                           'img_raw' : tf.FixedLenFeature([], tf.string),
                                       })

    img = tf.decode_raw(features['img_raw'], tf.uint8)
    img = tf.reshape(img, [230400])
    img = tf.cast(img, tf.float32) * (1. / 255) - 0.5
    label = tf.cast(features['label'], tf.int64)

    return img, label

# def compute_accuracy(v_xs,v_ys):
#     global prediction
#     y_pre = sess.run(prediction,feed_dict={xs:v_xs})
# #    correct_prediction = tf.equal(tf.argmax(y_pre,1),tf.arg_max(v_ys,1))
#     correct_prediction = tf.equal(tf.argmax(y_pre,1),tf.argmax(v_ys,1))
#     accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))
#     result = sess.run(accuracy,feed_dict={xs:v_xs,ys:v_ys})
#     return result


img, label = read_and_decode("frog.tfrecords")
# print(img.shape)
# print(label.shape)

x = tf.placeholder(tf.float32, [None, 230400])
W = tf.Variable(tf.zeros([230400, 1]))
b = tf.Variable(tf.zeros([1]))
y = tf.matmul(x, W) + b
y_ = tf.placeholder(tf.float32, [None, 1])
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)



img_batch, label_batch = tf.train.shuffle_batch([img, label],
                                                batch_size=500, capacity=10000,
                                                min_after_dequeue=100,
                                                num_threads=4,
                                                allow_smaller_final_batch=True)
saver = tf.train.Saver()

init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    # 启动队列
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess=sess,coord=coord)
    while True:
        try:
            for i in range(50):
                print(img_batch.shape, label_batch)
                val, l = sess.run([img_batch, label_batch])
                l = tf.one_hot(l-1,1).eval()
                print(l[0],l[1],l[2],l[3],l[4],l[5],'loop check')
                sess.run(train_step, feed_dict={x: val, y_: l})
                if i % 10 == 0:
                    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
                    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
                    print(sess.run(accuracy, feed_dict={x: val,
                                                        y_: l}))
                print('goes here')
        except tf.errors.OutOfRangeError:
            print('error')
            break

    coord.request_stop()
    coord.join(threads)
    save_path = saver.save(sess,"my_net/save_basic_net.ckpt")
    print("Save to path:",save_path)


# saver = tf.train.Saver()
#
# with tf.Session() as sess:
#     saver.restore(sess,"my_net/save_net.ckpt")
#     print('weight',sess.run(W))
#     print('bias',sess.run(b))