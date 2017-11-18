# -*- coding: utf-8 -*-

# author:Lichang

import tensorflow as tf

def read_and_decode(filename):
    #根据文件名生成一个队列
    filename_queue = tf.train.string_input_producer([filename])

    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)
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

img, label = read_and_decode("frog.tfrecords")

img_batch, label_batch = tf.train.shuffle_batch([img, label],
                                                batch_size=500, capacity=10000,
                                                min_after_dequeue=100,
                                                num_threads=4,
                                                allow_smaller_final_batch=True)

Ir = 0.001  # learning rate
# training_iters = 10000  # train step upper limit
batch_size = 500
# n_steps = 240
n_inputs = 230400
n_hidden_units = 128
n_classes = 1

x = tf.placeholder(tf.float32, [None, n_inputs])
y = tf.placeholder(tf.float32, [None, n_classes])

weights = {
    # shape (28,128)
    'in':  tf.Variable(tf.random_normal([n_inputs, n_hidden_units])),
    'out': tf.Variable(tf.random_normal([n_hidden_units, n_classes]))
}

biases = {
    # shape 128
    'in': tf.Variable(tf.constant(0.1, shape=[n_hidden_units, ])),
    # shape 10
    'out': tf.Variable(tf.constant(0.1, shape=[n_classes, ]))
}

def RNN(X, weights, biases):

    # X = tf.reshape(X, [-1, n_inputs])
    # # 128 btach * 28 steps, 128 hidden
    X_in = tf.matmul(X, weights['in']) + biases['in']
    # # 128 batch, 28 steps, 128 hidden
    # print(X_in.shape)
    X_in = tf.reshape(X_in, [-1, 240, n_hidden_units, ])

    lstm_cell = tf.nn.rnn_cell.BasicLSTMCell(n_hidden_units, forget_bias=0.1, state_is_tuple=True)
    _init_state = lstm_cell.zero_state(batch_size, dtype=tf.float32)

    # outputs, states = tf.nn.dynamic_rnn(lstm_cell, X_in, initial_state=_init_state, time_major=False)
    outputs, states = tf.nn.dynamic_rnn(lstm_cell, X_in, initial_state=_init_state, time_major=False)

    results = tf.matmul(states[1], weights['out']) + biases['out']
    return results

pred = RNN(x, weights, biases)
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y))
train_op = tf.train.AdamOptimizer(Ir).minimize(cost)

correct_pred = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

saver = tf.train.Saver()

init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    # 启动队列
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess=sess, coord=coord)
    try:
        for i in range(50):
            val, l = sess.run([img_batch, label_batch])
            sess.run([train_op], feed_dict={x: val, y: l})

            if i % 5 == 0:
                print(sess.run(accuracy, feed_dict={
                    y: l
                }))
    except:
        pass

    coord.request_stop()
    coord.join(threads)
    save_path = saver.save(sess,"my_net/save_RNN_net.ckpt")
    print("Save to path:",save_path)

################################################################
