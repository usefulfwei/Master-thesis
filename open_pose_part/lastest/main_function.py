# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 19:24:16 2017

@author: User
"""


'''
0 
1 脖子
2 左肩
3 左肘
4 左腕
5 右肩
6 右肘
7 右腕
8 
9
10
11
12
13

14 左眉峰
15 右眉峰

'''



import os
from Tkinter import *
import VideoCapture
import msvcrt
import json
import numpy as np
import time
import math

#function part

def quick_snap(cap):
    time.sleep(0.1)
    pic_name = int(time.time()*10)
    cap.getImage(timestamp=1).save(str(pic_name) + '.jpg')

def runCMD(path,command):
    originalPath = os.getcwd()
    os.chdir(path)
    os.system(command)
    os.chdir(originalPath)

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
            if len(new_dict["people"]) == 0:
                return []
            elif len(new_dict["people"]) == 1:
#                print np.array(new_dict["people"][0]["pose_keypoints"], dtype=np.float32).reshape((18, 3))
                return np.array(new_dict["people"][0]["pose_keypoints"], dtype=np.float32).reshape((18, 3))
            else:
                arr = []
                for i in range(len(new_dict["people"])):
#                    print np.array(new_dict["people"][i]["pose_keypoints"], dtype=np.float32).reshape((18, 3))
                    arr.append(np.array(new_dict["people"][i]["pose_keypoints"], dtype=np.float32).reshape((18, 3)))
                return arr


def eura_distance(arr1,arr2):
    return math.sqrt(pow(abs(arr1[0]-arr2[0]),2)+pow(abs(arr1[1]-arr2[1]),2))


def close_peer(array,limitation = 1.0,*args):
    relative_length = 0
    if array[3, 2] > 0.5 and array[4, 2] > 0.5:
        relative_length = eura_distance(array[3], array[4])
    elif array[6, 2] > 0.5 and array[7, 2] > 0.5:
        relative_length = eura_distance(array[6], array[7])
    if relative_length != 0:
        for i in args:
            p1 = i[0]
            p2 = i[1]
            if eura_distance(array[p1],array[p2]) > relative_length/limitation:
                return None
        else:
            return True
    else:
        return None

def slope_judge(arr1,arr2,arr3,limitation = 1.0):
    if abs(arr1[0]-arr2[0]) < limitation & abs(arr2[0]-arr3[0]) < limitation:
        return True
    elif abs(arr1[0]-arr2[0]) < limitation or abs(arr2[0]-arr3[0]) < limitation:
        return False
    else:
        slope1 = float(arr1[1]-arr2[1])/(arr1[0]-arr2[0])
        slope2 = float(arr2[1]-arr3[1])/(arr2[0]-arr3[0])
        if abs(slope1-slope2) < limitation:
            return True
        else:
            return False

def handshaking(arr1,arr2,r_min,r_max):
    if r_min <= eura_distance(arr1[4],arr2[4]) <= r_max or r_min <= eura_distance(arr1[7],arr2[7]) <= r_max:
        return True
    else:
        return False
    

'''
cold:
    double arms  single arms
        close_peer  3  7      4  6 or both     4  7  1
    feet shaking action slope
hot:
    T-shirt
        close_peer 4 1  or  7  1 only single and handshaking
    head
        close_peer()  4 0     7  0
    hand shake
        4 y >= 2 y   7 y >= 5 y   handshaking
    
    handshaking  
    original XY    current XY
    r  R
'''

def posture_decode(arr):
    print arr,'arr'
    print arr.shape
    relative_length = 0
    if arr[3,2] > 0.5 and arr[4,2] > 0.5:
        relative_length = eura_distance(arr[3],arr[4])
    elif arr[6,2] > 0.5 and arr[7,2] > 0.5:
        relative_length = eura_distance(arr[6],arr[7])
    print(relative_length,'relative')
    print(math.sqrt(pow(abs(arr[4, 0] - arr[6, 0]), 2) + pow(abs(arr[4, 1] - arr[6, 1]), 2)),'1')
    print(math.sqrt(pow(abs(arr[7, 0] - arr[3, 0]), 2) + pow(abs(arr[7, 1] - arr[3, 1]), 2)) ,'2')
    print(math.sqrt(pow(abs(arr[4, 0] - arr[0, 0]), 2) + pow(abs(arr[4, 1] - arr[0, 1]), 2)),'3')
    print(math.sqrt(pow(abs(arr[7, 0] - arr[0, 0]), 2) + pow(abs(arr[7, 1] - arr[0, 1]), 2)),'4')
    if relative_length != 0:
        if eura_distance(arr[4],arr[6]) < relative_length/1.5 or eura_distance(arr[7],arr[3]) < relative_length/1.5:
            return 'cold'
        elif eura_distance(arr[4],arr[0]) < relative_length/1.5 or eura_distance(arr[7],arr[0]) < relative_length/1.5:
            return 'hot'
    else:
        return None

def deleteImg(imgPath):
    originalPath = os.getcwd()
    os.chdir(imgPath)
    fileList = os.listdir(imgPath)
    for filename in fileList:
        pathTmp = os.path.join(imgPath,filename)
        os.remove(pathTmp)
    os.chdir(originalPath)

def deleteJson(json_arr,index):
    for i in range(index):
        os.remove(json_arr[i])

#static_value part
root_path = r'c:\openpose-master'
command = r'windows\x64\Release\OpenPoseDemo.exe -image_dir examples\static -write_keypoint_json examples/static_json -no_display -render_threshold 0.3 -write_images examples/img_data'
img_path = r'c:\openpose-master\examples\static'
img_json_path = r'c:\openpose-master\examples\static_json'
command = r'windows\x64\Release\OpenPoseDemo.exe -image_dir examples\action -write_keypoint_json examples/action_json -no_display -render_threshold 0.3 -write_images examples/img_data'
action_path = r'c:\openpose-master\examples\action'
action_json_path = r'c:\openpose-master\examples\action_json'
    
if __name__ == '__main__':
    cap = VideoCapture.Device(devnum=0,showVideoWindow=0)
    os.chdir(img_path)
    json_arr = []
    while True:
        time.sleep(0.1)
        pic_name = int(time.time()*10)
        cap.getImage(timestamp=1).save(str(pic_name)+'.jpg')
        print 'start taking picture'
        runCMD(root_path,command)
        get_all_json(json_path,json_arr)
        for i in json_arr:#
            arr = decode_arr(i)
            if len(arr) == 0:
                continue
            elif len(arr) == 18:
                print posture_decode(arr)
            else:
                for i in arr:
                    print posture_decode(i)