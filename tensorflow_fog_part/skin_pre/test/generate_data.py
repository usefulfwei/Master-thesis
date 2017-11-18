# -*- coding: utf-8 -*-

# author:Lichang

import xlrd
import os
import tensorflow as tf
from PIL import Image
import cv2

T_info = {}

temp_arr = []
form_path = r'./form/'

for file in os.listdir(form_path):
    pathTmp = os.path.join(form_path, file)
    workbook = xlrd.open_workbook(pathTmp)
    sheet = workbook.sheet_by_index(0)
    result = [file]
    for row in range(2, sheet.nrows):
        print(sheet.cell(row, 1).value)
        result.append(sheet.cell(row, 1).value)
    print(result)
    temp_arr.append(result)

for arr in temp_arr:
    if arr[0][:1] not in T_info.keys():
        temp = []
        for i in range(1, len(arr)-1):
            temp.append(arr[i])
            gap = round((arr[i+1] - arr[i]) / 11, 4)
            for j in range(11):
                temp.append(arr[i] + gap)
        temp.append(arr[len(arr)-1])
        T_info[arr[0][:1]] = temp

print(T_info, 't_info')

#制作二进制数据
file = "skin_train.tfrecords"
video_path = './combined_video/'

def create_record(filename = file):
    writer = tf.python_io.TFRecordWriter(filename)
    for name in os.listdir(video_path):
        print(name, 'videoname')
        video_file = os.path.join(video_path, name)
        labels = T_info[name[:1]]
        print(labels)
        index = 0
        count = 0
        cap = cv2.VideoCapture(video_file)
        # while (cap.isOpened()):
        ret, frame = cap.read()
        while ret == True:
            count += 1
            if count % 150 == 0:
                index += 1
            img_raw = frame[:, 650:1200].tobytes()
            print([labels[index]], 'asgaf')
            example = tf.train.Example(
                features=tf.train.Features(feature={
                    "label": tf.train.Feature(float_list=tf.train.FloatList(value=[labels[index]])),
                    'img_raw': tf.train.Feature(bytes_list=tf.train.BytesList(value=[img_raw]))
                }))
            writer.write(example.SerializeToString())
            ret, frame = cap.read()
    writer.close()


create_record()