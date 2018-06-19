# coding:utf-8
import sys

import tensorflow as tf
import numpy as np
import result_data
import get_data


# 添加隐藏层
def add_layer(inputs, in_size, out_size, activation_func=None, keep=None, layer_name=None):
    if layer_name is None:
        layer_name = 'layer'
    with tf.name_scope(layer_name):
        loc_w = tf.Variable(tf.random_normal([in_size, out_size]))
        loc_b = tf.Variable(tf.zeros([1, out_size]) + 0.1)
        loc_output = tf.matmul(inputs, loc_w) + loc_b
        if keep is not None:
            loc_output = tf.nn.dropout(loc_output, keep)
        if activation_func is not None:
            loc_output = activation_func(loc_output)
    tf.summary.histogram(layer_name + '/outputs', loc_output)
    return loc_output


BATCH = 1000
KEEP_ = 0.5
LEARN_RATE_START = 0.002
TRAIN_TIMES = 2000
DIFF_RATE = 0.7
TRAIN_DATA_RATE = 0
STORE_PATH = 'final/train/saver.ckpt'

x_data = get_data.get_mat_23(TRAIN_DATA_RATE, sys.maxsize)
y_data = result_data.get_reality_for_train(TRAIN_DATA_RATE, sys.maxsize)

DATA_SIZE = x_data.shape[0]
SIZE_X = x_data.shape[1]

test_x = get_data.get_mat_23(0, TRAIN_DATA_RATE)
test_y = result_data.get_reality_for_test(0, TRAIN_DATA_RATE)
TEST_SIZE = test_x.shape[0]

if x_data.shape[0] != y_data.shape[0]:
    print('error , x_data.shape[0] != y_data.shape[0]')
    exit()
# if test_x.shape[1] != x_data.shape[1]:
#     print('error , test_x.shape[1] != x_data.shape[1]')
#     exit()
# if test_x.shape[0] != test_y.shape[0]:
#     print('error , test_x.shape[0] != test_y.shape[0]')
#     exit()

holder_x = tf.placeholder(tf.float32, [None, SIZE_X])
holder_y = tf.placeholder(tf.float32, [None, 1])
keep_prob = tf.placeholder(tf.float32)

learn_rate = tf.Variable(LEARN_RATE_START, dtype=tf.float32)

l_1 = add_layer(holder_x, SIZE_X, 25, activation_func=tf.nn.tanh, keep=keep_prob, layer_name='layer_1')
produce = add_layer(l_1, 25, 1, activation_func=tf.nn.sigmoid, keep=keep_prob, layer_name='layer_out')

with tf.name_scope('loss'):
    loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=holder_y, logits=produce))
    # loss = tf.reduce_mean(-tf.reduce_sum(holder_y * tf.log(produce), reduction_indices=[1]))  # loss
    # loss = tf.reduce_mean(tf.reduce_sum(tf.square(holder_y - produce), reduction_indices=[1]))  # 损失函数
    tf.summary.scalar('loss', loss)

train_step = tf.train.AdamOptimizer(learn_rate).minimize(loss)
saver = tf.train.Saver()
init = tf.global_variables_initializer()


def train():
    with tf.Session() as sess:
        sess.run(init)
        for i in range(TRAIN_TIMES):
            # 指数下降学习率，不一定有用
            sess.run(tf.assign(learn_rate, LEARN_RATE_START * (0.80 ** (i/100))))
            for j in range(int(DATA_SIZE / BATCH)):
                start = (j * BATCH) % DATA_SIZE
                end = start + BATCH
                batch_x = x_data[start:end]
                batch_y = y_data[start:end]
                sess.run(train_step, feed_dict={holder_x: batch_x, holder_y: batch_y, keep_prob: KEEP_})
                if j % 50 == 0:
                    pass
            loss_rate = sess.run(loss, feed_dict={holder_x: x_data, holder_y: y_data, keep_prob: 1})
            # test_result = sess.run(produce, feed_dict={holder_x: test_x, keep_prob: 1})
            # print('test', compute_dif(test_result, test_y))
            print(i, loss_rate, '\n')
            saver.save(sess=sess, save_path=STORE_PATH)


# 测试时计算预测值和真实值的差别
def compute_dif(result, reality):
    global DIFF_RATE
    for i in range(result.shape[0]):
        if result[i][0] >= DIFF_RATE:
            result[i][0] = 1
        else:
            result[i][0] = 0
    return np.mean(np.equal(result, reality))


def test():
    # for test
    global saver
    global init
    global DIFF_RATE
    with tf.Session() as sess:
        sess.run(init)

        # saver.restore(sess, STORE_PATH)

        test_result = sess.run(produce, feed_dict={holder_x: test_x, keep_prob: 1})
        print('test', compute_dif(test_result, test_y))
        # for i in range(TEST_SIZE):
        #     print(i, test_result[i], test_y[i])
        result = 0
        for i in range(500):
            DIFF_RATE = DIFF_RATE + 1 / 1000.0
            result = max(result, compute_dif(test_result, test_y))
            print(i, compute_dif(test_result, test_y))

        # print('max', result)


def produce_final():
    global saver
    global init
    global DIFF_RATE
    with tf.Session() as sess:
        sess.run(init)
        saver.restore(sess, STORE_PATH)
        data_all = get_data.get_mat_30()
        result = sess.run(produce, feed_dict={holder_x: data_all, keep_prob: 1})
        for i in range(result.shape[0]):
            if result[i][0] >= 0.6:
                result[i][0] = 1
            else:
                result[i][0] = 0
        users_id_all = get_data.get_all_users_id()
        print(users_id_all.shape, result.shape)
        with open('final/final.txt', 'w') as file:
            for i in range(result.shape[0]):
                if result[i] == 1:
                    file.write(str(int(users_id_all[i])) + '\n')


produce_final()
# test()
# train()
