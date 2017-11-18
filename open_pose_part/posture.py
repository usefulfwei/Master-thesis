# -*- coding: utf-8 -*-

# author:Lichang

'''
1 脖子
2 左肩
3 左肘
4 左腕
5 右肩
6 右肘
7 右腕
0 眉心
14 左眉峰
15 右眉峰

'''

import os
import json
import numpy as np
import time
import math

# data/
def get_all_json(path,json_arr):
    fileList = os.listdir(path)
    for filename in fileList:
        pathTmp = os.path.join(path,filename)
        if os.path.isdir(pathTmp):
            get_all_json(pathTmp,json_arr)
        elif filename[-5:].upper() == '.JSON':
            json_arr.append(pathTmp)
    return json_arr
# json_list --> decode_arr

# path 'data/cold1_keypoints.json'
def decode_arr(path):
    if os.access(path,os.F_OK):
        with open(path) as f:
            all_text = f.read()
            new_dict = json.loads(all_text)
            f.close()
            if len(new_dict["people"]) == 1:
                return np.array(new_dict["people"][0]["pose_keypoints"], dtype=np.float32).reshape((18, 3))
            else:
                arr = []
                for i in range(len(new_dict["people"])):
                    arr.extend(np.array(new_dict["people"][i]["pose_keypoints"], dtype=np.float32).reshape((18, 3)))
                return arr
arr = decode_arr('data/cold2_keypoints.json')
# print(arr)
print(arr.shape)
# print(arr[3,0])
# print(arr[3,1])

def eura_distance(arr1,arr2):
    return math.sqrt(pow(abs(arr1[0]-arr2[0]),2)+pow(abs(arr1[1]-arr2[1]),2))

def posture_decode(arr):
    relative_length = 0
    if arr[3,2] > 0.5 and arr[4,2] > 0.5:
        relative_length = eura_distance(arr[3],arr[4])
    elif arr[6,2] > 0.5 and arr[7,2] > 0.5:
        relative_length = eura_distance(arr[6],arr[7])
    # print(relative_length,'relative')
    # print(math.sqrt(pow(abs(arr[4, 0] - arr[6, 0]), 2) + pow(abs(arr[4, 1] - arr[6, 1]), 2)),'1')
    # print(math.sqrt(pow(abs(arr[7, 0] - arr[3, 0]), 2) + pow(abs(arr[7, 1] - arr[3, 1]), 2)) ,'2')
    # print(math.sqrt(pow(abs(arr[4, 0] - arr[0, 0]), 2) + pow(abs(arr[4, 1] - arr[0, 1]), 2)),'3')
    # print(math.sqrt(pow(abs(arr[7, 0] - arr[0, 0]), 2) + pow(abs(arr[7, 1] - arr[0, 1]), 2)),'4')
    if relative_length != 0:
        if eura_distance(arr[4],arr[6]) < relative_length/1.5 or eura_distance(arr[7],arr[3]) < relative_length/1.5:
            return ('cold')
        elif eura_distance(arr[4],arr[0]) < relative_length/1.5 or eura_distance(arr[7],arr[0]) < relative_length/1.5:
            return ('hot')
    else:
        return ('not clear for analysing')

print(posture_decode(arr))