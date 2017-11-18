# -*- coding: utf-8 -*-

# author:Lichang

from sklearn.cross_validation import train_test_split
import tensorflow as tf
import pickle

FLAGS = None

file_path = r'./data/data.pkl'

pkl_file = pickle.loads(file_path)

data = pickle.load(pkl_file)

pkl_file.close()

X = data.images
y = data.labels

input_size = len(X[0])
# 320 * 240 = 76800
single_dimension = int(input_size//3)
output_size = len(y[0])
instance = len(X)


X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = .2)


def deepnn(x):
    # Reshape to use within a convolutional neural net.
    # Last dimension is for "features" - there is only one here, since images are
    # grayscale -- it would be 3 for an RGB image, 4 for RGBA, etc.
    x_image = tf.reshape(x, [-1, 320, 240, 3])
    # 3 for RGB
    # W_conv1 = weight_variable([5, 5, 3, output_size])
    W_conv1 = weight_variable([5, 5, 3, 96])

    # b_conv1 = bias_variable([output_size])
    b_conv1 = bias_variable([96])

    h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
    # 320 240 * 96

    h_pool1 = max_pool_2x2(h_conv1)
    # 160 120 * 96

    W_conv2 = weight_variable([5, 5, 96, 384])
    b_conv2 = bias_variable([384])
    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)

    h_pool2 = max_pool_2x2(h_conv2)
    # 80 60 384

    W_fc1 = weight_variable([80 * 60 * 384, 1024])
    b_fc1 = bias_variable([1024])

    h_pool2_flat = tf.reshape(h_pool2, [-1, 80 * 60 * 384])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

    keep_prob = tf.placeholder(tf.float32)
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    W_fc2 = weight_variable([1024, output_size])
    b_fc2 = bias_variable([output_size])

    y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2

    return y_conv, keep_prob

def conv2d(x, W):
    """conv2d returns a 2d convolution layer with full stride."""
    '''first and final one must be 1 
    strides [1, x_movement, y_movement, 1]
    padding: SAME keep same size  VALID smaller
    '''
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
    """max_pool_2x2 downsamples a feature map by 2X."""
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                        strides=[1, 2, 2, 1], padding='SAME')


def weight_variable(shape):
    """weight_variable generates a weight variable of a given shape."""
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    """bias_variable generates a bias variable of a given shape."""
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


def main(_):
  # Import data
  x = tf.placeholder(tf.float32, [None, input_size])
  y_ = tf.placeholder(tf.float32, [None, output_size])

  y_conv, keep_prob = deepnn(x)

  cross_entropy = tf.nn.softmax_cross_entropy_with_logits(labels=y_,
                                                            logits=y_conv)
  cross_entropy = tf.reduce_mean(cross_entropy)

  train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

  correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
  correct_prediction = tf.cast(correct_prediction, tf.float32)
  accuracy = tf.reduce_mean(correct_prediction)


  with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    # for i in range(10000):
    #   # batch = data.train.next_batch(50)
    #   if i % 100 == 0:
    #     train_accuracy = accuracy.eval(feed_dict={
    #         x: batch[0], y_: batch[1], keep_prob: 1.0})
    #     print('step %d, training accuracy %g' % (i, train_accuracy))
    train_step.run(feed_dict={x: X_train, y_: y_train, keep_prob: 0.5})

    print('test accuracy %g' % accuracy.eval(feed_dict={
        x: X_test, y_: y_test, keep_prob: 1.0}))
