# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 19:24:16 2017

@author: Lichang
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



import os
from Tkinter import *
import VideoCapture
import msvcrt
import json
import numpy as np
import time
import math


root_path = r'c:\openpose-master'
command = r'windows\x64\Release\OpenPoseDemo.exe -image_dir examples\static -write_keypoint_json examples/static_json -no_display -render_threshold 0.1 -write_images examples/img_data'
img_path = r'c:\openpose-master\examples\static'
img_json_path = r'c:\openpose-master\examples\static_json'
action_command = r'windows\x64\Release\OpenPoseDemo.exe -image_dir examples\action -write_keypoint_json examples/action_json -no_display -render_threshold 0.1 -write_images examples/img_data'
action_path = r'c:\openpose-master\examples\action'
action_json_path = r'c:\openpose-master\examples\action_json'
    

#function part

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

def decode_arr(path):
    if os.access(path,os.F_OK):
        with open(path) as f:
            all_text = f.read()
            new_dict = json.loads(all_text)
            f.close()
            if len(new_dict["people"]) == 0:
                return []
            elif len(new_dict["people"]) == 1:
                return np.array(new_dict["people"][0]["pose_keypoints"], dtype=np.float32).reshape((18, 3))
            else:
                arr = []
                for i in range(len(new_dict["people"])):
                    arr.append(np.array(new_dict["people"][i]["pose_keypoints"], dtype=np.float32).reshape((18, 3)))
                return arr

def eura_distance(arr1,arr2):
    return math.sqrt(pow(abs(arr1[0]-arr2[0]),2)+pow(abs(arr1[1]-arr2[1]),2))



def close_peer(array,peer,limitation = 1.5):
    relative_length = 0
    if array[3, 2] > 0.5 and array[4, 2] > 0.5:
        relative_length = eura_distance(array[3], array[4])
    elif array[6, 2] > 0.5 and array[7, 2] > 0.5:
        relative_length = eura_distance(array[6], array[7])
    if relative_length != 0:
        for i in peer:
            p1 = i[0]
            p2 = i[1]
            if p1 > 10 and p2 > 10:
                print eura_distance(array[p1],array[p2])
            if eura_distance(array[p1],array[p2]) > relative_length/limitation:
                return None
        else:
            return True
    else:
        return None

def slope_judge(arr1,arr2=[],difference = 30.0):
    def _slope_judge(arr1,arr2,arr3):
        if int(arr1[0]) == 0 or int(arr2[0]) == 0 or int(arr3[0]) == 0:
            return None
        else:
            slope1 = float(arr1[1]-arr2[1])/(arr1[0]-arr2[0])
            slope2 = float(arr2[1]-arr3[1])/(arr2[0]-arr3[0])
            if abs(slope1-slope2) < difference:
                return 'straight'
            else:
                return 'bending'
    if arr2 == []:
        if _slope_judge(arr1[8],arr1[9],arr1[10]) is not None and _slope_judge(arr1[11],arr1[12],arr1[13]) is not None and \
            (_slope_judge(arr1[8],arr1[9],arr1[10]) != _slope_judge(arr1[11],arr1[12],arr1[13])):
                return True
        else:
            return False
    else:
        if _slope_judge(arr1[8],arr1[9],arr1[10]) != _slope_judge(arr2[8],arr2[9],arr2[10]) or \
        _slope_judge(arr1[11],arr1[12],arr1[13]) != _slope_judge(arr2[11],arr2[12],arr2[13]):
            return True
        else:
            return False                       
    

def handshaking(arr1,arr2,r_min=2.0,r_max=120.0):
    print eura_distance(arr1[4],arr2[4])
    print eura_distance(arr1[7],arr2[7])
    if r_min <= eura_distance(arr1[4],arr2[4]) <= r_max or r_min <= eura_distance(arr1[7],arr2[7]) <= r_max:
        return True
    else:
        return False

def hot_shirt_zone(arr):
    if 0 in [int(arr[8][1]),int(arr[11][1]),int(arr[5][0]),int(arr[6][0])]:
        return False
    elif max(arr[2][0],arr[3][0]) < arr[4][0] < min(arr[5][0],arr[6][0]) and max(arr[1][1],arr[2][1],arr[5][1]) < arr[4][1] < min(arr[8][1],arr[11][1]) or \
       max(arr[2][0],arr[3][0]) < arr[7][0] < min(arr[5][0],arr[6][0]) and max(arr[1][1],arr[2][1],arr[5][1]) < arr[7][1] < min(arr[8][1],arr[11][1]):
            return True
    else:
        return False

def hot_swap_zone(arr):
    if (arr[4][1] < arr[3][1] and  arr[3][0]<arr[4][0]<arr[1][0]) or \
    (arr[7][1] < arr[6][1] and  arr[1][0]<arr[7][0]<arr[6][0]):
        return True
    else:
        return False

def judge_pose(arr,cap):
    if close_peer(arr,[[3,7]],limitation=1.5) or close_peer(arr,[[4,6]],limitation=1.5):
        return 'cold arms'
    elif close_peer(arr,[[4,16]],limitation=1.4) or close_peer(arr,[[7,17]],limitation=1.4):
        return 'hot head'
    elif slope_judge(arr):
        originalArr = arr
        originalPath = os.getcwd()
        os.chdir(action_path)
        for _ in range(5):
            time.sleep(0.3)
            pic_name = int(time.time()*100)
            cap.getImage(timestamp=1).save(str(pic_name)+'.jpg')
        runCMD(root_path,action_command)
        action_json = []
        get_all_json(action_json_path,action_json)
        for i in range(len(action_json)):
            arr = decode_arr(action_json[i])
            if len(arr) == 0:
                continue
            elif len(arr) == 18:
                if slope_judge(originalArr,arr):
                    originalArr = arr
                    continue
                else:
                    deleteImg(action_path)
                    deleteJson(action_json)
                    os.chdir(originalPath)
                    print 'duojiao fail'
                    return 'Cannot figure the posture'
            else:
                for i in arr:
                     if slope_judge(originalArr,i):
                        originalArr = i
                        continue
                     else:
                        deleteImg(action_path)
                        deleteJson(action_json)
                        os.chdir(originalPath)
                        print 'duojiao fail'
                        return 'Cannot figure the posture'
        else:
            deleteImg(action_path)
            deleteJson(action_json)
            os.chdir(originalPath)
            return 'cold_stomping_action'
    elif hot_swap_zone(arr):
        originalArr = arr
        originalPath = os.getcwd()
        os.chdir(action_path)
        deleteImg(action_path)
        for _ in range(10):
            time.sleep(0.2)
            pic_name = int(time.time()*100)
            cap.getImage(timestamp=1).save(str(pic_name)+'.jpg')
        runCMD(root_path,action_command)
        action_json = []
        get_all_json(action_json_path,action_json)
        count = 0
        for i in range(len(action_json)):
            arr = decode_arr(action_json[i])
            if len(arr) == 0:
                continue
            elif len(arr) == 18:
                if handshaking(originalArr,arr):
                    count += 1
                    originalArr = arr
                    continue
            else:
                for i in arr:
                    if handshaking(originalArr,i):
                        count += 1
                        originalArr = i
                        continue
                    
        deleteImg(action_path)
        deleteJson(action_json)
        os.chdir(originalPath)                
        if count >= 3:
            return 'hot_hand_swap'
        else:
            print 'shanfeng fail'
            return 'Cannot figure the posture'
    elif hot_shirt_zone(arr):
        originalArr = arr
        originalPath = os.getcwd()
        os.chdir(action_path)
        deleteImg(action_path)
        for _ in range(10):
            time.sleep(0.2)
            pic_name = int(time.time()*100)
            cap.getImage(timestamp=1).save(str(pic_name)+'.jpg')
        runCMD(root_path,action_command)
        action_json = []
        get_all_json(action_json_path,action_json)
        count = 0
        for i in range(len(action_json)):
            arr = decode_arr(action_json[i])
            if len(arr) == 0:
                continue
            elif len(arr) == 18:
                if handshaking(originalArr,arr):
                    count += 1
                    originalArr = arr
                    continue
            else:
                for i in arr:
                    if handshaking(originalArr,i):
                        count += 1
                        originalArr = i
                        continue
        deleteImg(action_path)
        deleteJson(action_json)
        os.chdir(originalPath)
        if count >= 3:
            return 'hot_shirt_action'
        else:
            print ' fail shirt'
            return 'Cannot figure the posture'
    else:
        print 'cannot goes into action'
        return 'Cannot figure the posture'

def deleteImg(imgPath):
    originalPath = os.getcwd()
    os.chdir(imgPath)
    fileList = os.listdir(imgPath)
    for filename in fileList:
        pathTmp = os.path.join(imgPath,filename)
        os.remove(pathTmp)
    os.chdir(originalPath)

def deleteJson(json_arr):
    for i in json_arr:
        os.remove(i)

def start_cleaning(arr):
    originalPath = os.getcwd()
    for i in arr:
        os.chdir(i)
        fileList = os.listdir(i)
        for fileName in fileList:
            pathTmp = os.path.join(i,fileName)
            os.remove(pathTmp)
    os.chdir(originalPath)

#static_value part
        
'''
root_path = r'c:\openpose-master'
command = r'windows\x64\Release\OpenPoseDemo.exe -image_dir examples\static -write_keypoint_json examples/static_json -no_display -render_threshold 0.1 -write_images examples/img_data'
img_path = r'c:\openpose-master\examples\static'
img_json_path = r'c:\openpose-master\examples\static_json'
action_command = r'windows\x64\Release\OpenPoseDemo.exe -image_dir examples\action -write_keypoint_json examples/action_json -no_display -render_threshold 0.1 -write_images examples/img_data'
action_path = r'c:\openpose-master\examples\action'
action_json_path = r'c:\openpose-master\examples\action_json'
'''

if __name__ == '__main__':
    print 'program starts'
    start_cleaning([img_path,img_json_path,action_path,action_json_path])
    cap = VideoCapture.Device(devnum=0,showVideoWindow=0)
    os.chdir(img_path)
    json_arr = []
    while True:
#        if ord(msvcrt.getch()) in [81,113]:
#            break
        if len(os.listdir(img_path)) <= 3:
            time.sleep(0.5)
            pic_name = int(time.time()*10)
            cap.getImage(timestamp=1).save(str(pic_name)+'.jpg')
            print 'start taking picture'
        else:
            runCMD(root_path,command)
            get_all_json(img_json_path,json_arr)
            for i in json_arr:
                arr = decode_arr(i)
                if arr is None or len(arr) == 0:
                    continue
                elif len(arr) == 18:
                    if judge_pose(arr,cap) != 'Cannot figure the posture':
                        print judge_pose(arr,cap)
                        break
                else:
                    for i in arr:
                        if judge_pose(i,cap) != 'Cannot figure the posture':
                            print judge_pose(i,cap)
                            break
            deleteImg(img_path)
            deleteJson(json_arr)
            json_arr = []