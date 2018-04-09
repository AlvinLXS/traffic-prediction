import os
import numpy as np


def split_by_time(data, timestamp, split_time):
    """
    divide data into two subsets: Train & Test
    """
    assert(len(data) == len(timestamp))
    assert(split_time in set(timestamp))
    data_train = []
    time_train = []
    data_test = []
    time_test = []
    flag = False
    for t, d in zip(timestamp, data):
        if t == split_time:
            flag = True
        if flag is False:
            data_train.append(d)
            time_train.append(t)
        else:
            data_test.append(d)
            time_test.append(t)
    return (np.asarray(data_train), time_train), (np.asarray(data_test), time_test)


def get_file_name(path):
    """
    Get the file name in the folder
    """
    files = []
    for file in os.listdir(path):
        files.append(file)
    files.sort()
    return files


def get_time_list(filename):
    """
    Get time list from the txt file
    """
    f = open(filename, 'r')
    time_all = []
    for line in f.readlines():
        temp = line.strip('\n')
        time_all.append(temp)
    return time_all
