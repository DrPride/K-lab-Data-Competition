# coding:utf-8
import os
import numpy as np
import sys

REGISTER_FILE = 'data/user_register_log.txt'
INPUT_FILE = 'data/app_launch_log.txt'
OUTPUT_FILE_TRAIN = 'output/reality_train.txt'
OUTPUT_FILE_TEST = 'output/reality_test.txt'
USER_SIZE = 500000
DATE_SIZE = 23


def get_users_id(min_id, max_id, date_left, date_right):
    users_id = []
    with open(REGISTER_FILE, 'r') as file:
        while True:
            line = file.readline()
            if line is '':
                break
            items = line.split('\t')
            user_id = int(items[0])
            date = int(items[1])
            if date_left <= date <= date_right:
                if min_id < user_id <= max_id:
                    users_id.append(user_id)
            #     if min_id is None:
            #         if user_id <= max_id:
            #             arr_result[user_id] = 0
            #     elif max_id is None:
            #         if user_id > min_id:
            #             arr_result[user_id] = 0
            # elif date > date_right:
            #     if min_id is None:
            #         if user_id <= max_id:
            #             arr_result[user_id] = 1
            #     elif max_id is None:
            #         if user_id > min_id:
            #             arr_result[user_id] = 1
    return users_id


def get_result_data(min_id, max_id, date_left, date_right, output_file=None):
    users_id = get_users_id(min_id, max_id, date_left, date_right)
    arr_result = {}
    for i in users_id:
        arr_result[i] = 0
    with open(INPUT_FILE, 'r') as file:
        while True:
            line = file.readline()
            if line is '':
                break
            items = line.split('\t')
            user_id = int(items[0])
            date = int(items[1])
            try:
                if date > date_right:
                    if min_id < user_id <= max_id:
                        temp = arr_result[user_id]  # 当没有这个key时可以被try-catch捕捉到
                        arr_result[user_id] = 1
            except(Exception):
                continue
    count = 0
    mat_result = np.zeros([len(arr_result), 1], np.float32)
    #
    sorted_result = sorted(arr_result.items(), key=lambda item: item[0])
    for i in sorted_result:
        mat_result[count][0] = i[1]
        count = count + 1
        if __name__ == '__main__':
            print(str(i), i[1])

    if output_file is not None:
        file = open(output_file, 'w')
        for i in sorted_result:
            file.write(str(i[0]) + '\t' + str(i[1]) + '\n')
        file.close()

    return mat_result


def get_reality_for_train(min_id,max_id):
    return get_result_data(max_id=max_id, min_id=min_id, date_left=0, date_right=DATE_SIZE,
                           output_file=OUTPUT_FILE_TRAIN)


def get_reality_for_test(min_id,max_id):
    return get_result_data(max_id=max_id, min_id=min_id, date_left=0, date_right=DATE_SIZE,
                           output_file=OUTPUT_FILE_TEST)


if __name__ == '__main__':
    print('for_test')
    get_reality_for_test()
    print('for_train')
    get_reality_for_train()
