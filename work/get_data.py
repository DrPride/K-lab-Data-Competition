# coding:utf-8

import pandas
import numpy as np
import sys

test1_file = "output/test.txt"
test2_file = "output/test2.csv"
test1_30_file = "output/test_30tian.txt"
test2_30_file = "output/test2_30tian.csv"
d_size = 32
test1_size = 19
test2_size = 13


def cvs_to_mat(min_id, max_id, file_name, size):
    arr = []
    cvs = pandas.read_csv(file_name)
    # result = cvs.drop(['days'], axis=1)
    result = cvs.values.astype('float32')
    for items in result:
        if min_id < float(items[0]) <= max_id:
            temp = []
            for i in range(1, size + 1):
                temp.append(items[i])
            arr.append(temp)
            # mat = np.append(mat, [np.array(temp)], axis=0)
    mat = np.mat(arr)
    return mat


def file_to_mat(min_id, max_id, file_name, size):
    mat = np.empty(shape=[0, size], dtype=np.float32)
    arr = []
    with open(file_name, 'r') as file:
        while True:
            line = file.readline()
            if line == '':
                break
            items = line.split('\t')
            if min_id < float(items[0]) <= max_id:
                temp = []
                for i in range(1, size + 1):
                    temp.append(items[i])
                arr.append(temp)
                # mat = np.append(mat, [np.array(temp)], axis=0)
                # mat = np.row_stack((mat, temp))
        mat = np.mat(arr)  # 直接用上面的矩阵运算要慢很多，不知道为什么
    return mat


def get_mat_23(min_id, max_id):
    mat_test1 = file_to_mat(min_id, max_id, test1_file, test1_size)
    mat_test2 = cvs_to_mat(min_id, max_id, test2_file, test2_size)
    return np.hstack((mat_test1, mat_test2))


def get_mat_30():
    min_id = 0
    max_id = sys.maxsize
    mat_test1 = file_to_mat(min_id, max_id, test1_30_file, test1_size)
    mat_test2 = cvs_to_mat(min_id, max_id, test2_30_file, test2_size)
    return np.hstack((mat_test1, mat_test2))


def get_all_users_id():
    arr = []
    cvs = pandas.read_csv(test2_30_file)
    result = cvs.values.astype('float32')
    for items in result:
        arr.append([items[0]])
    return np.mat(arr)


if __name__ == '__main__':
    print(get_mat_23(0, 500000).shape)
