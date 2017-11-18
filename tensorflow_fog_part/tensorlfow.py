# -*- coding: utf-8 -*-

# author:Lichang

from sklearn.cross_validation import train_test_split
import tensorflow as tf
import pickle

file_path = r'./data/data.pkl'

pkl_file = pickle.loads(file_path)

data = pickle.load(pkl_file)

pkl_file.close()

X = data.images
y = data.labels

input_size = len(X[0])
output_size = len(y[0])
instance = len(X)

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = .3)

def main(_):
    # Import data

    x = tf.placeholder(tf.float32, [None, input_size])
    W = tf.Variable(tf.zeros([input_size, output_size]))
    b = tf.Variable(tf.zeros([output_size]))
    y = tf.matmul(x, W) + b

    # Define loss and optimizer
    y_ = tf.placeholder(tf.float32, [None, output_size])

    cross_entropy = tf.reduce_mean(
        tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

    sess = tf.InteractiveSession()
    tf.global_variables_initializer().run()

    for _ in range(100):
        batch_xs, batch_ys = data.train.next_batch(instance//100)
        sess.run(train_step, feed_dict={x: X_train, y_: y_train})

    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    print(sess.run(accuracy, feed_dict={x: X_test,
                                        y_: y_test}))


if __name__ == '__main__':
    tf.app.run(main=main)