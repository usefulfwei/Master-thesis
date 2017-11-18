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


def close_peer(array,peer,limitation = 1.0):
    relative_length = 0
    if array[3, 2] > 0.5 and array[4, 2] > 0.5:
        relative_length = eura_distance(array[3], array[4])
    elif array[6, 2] > 0.5 and array[7, 2] > 0.5:
        relative_length = eura_distance(array[6], array[7])
    print relative_length,'relative length'
    if relative_length != 0:
        for i in peer:
            print i
            p1 = i[0]
            p2 = i[1]
            
            print eura_distance(array[p1],array[p2]) ,'limitation'
#            if eura_distance(array[p1],array[p2]) > relative_length/limitation:
#                return None
#        else:
#            return True
#    else:
#        return None

def slope_judge(arr1,arr2,arr3,difference = 30.0):
#    print 'x'
#    print abs(arr1[0]-arr2[0])
#    print abs(arr2[0]-arr3[0])
#    print 'slope'
#    print (arr1[1]-arr2[1])/(arr1[0]-arr2[0])
#    print (arr2[1]-arr3[1])/(arr2[0]-arr3[0])
    if int(arr1[0]) == 0 or int(arr2[0]) or int(arr3[0]):
        return None
    else:
        slope1 = float(arr1[1]-arr2[1])/(arr1[0]-arr2[0])
        slope2 = float(arr2[1]-arr3[1])/(arr2[0]-arr3[0])
        if abs(slope1-slope2) < difference:
            return 'straight'
        else:
            return 'bending'

def handshaking(arr1,arr2):
    print eura_distance(arr1[4],arr2[4]), '4r_min r_max'
    print eura_distance(arr1[7],arr2[7]), '7r_min r_max'
#    if r_min <= eura_distance(arr1[4],arr2[4]) <= r_max or r_min <= eura_distance(arr1[7],arr2[7]) <= r_max:
#        return True
#    else:
#        return False

def hot_shirt_zone(arr):
    if min(arr[2][0],arr[3][0]) <= arr[4][0] <= max(arr[5][0],arr[6][0]) and min(arr[1][1],arr[2][1],arr[5][1]) <= arr[4][1] <= max(arr[8][1],arr[11][1]) or \
       min(arr[2][0],arr[3][0]) <= arr[7][0] <= max(arr[5][0],arr[6][0]) and min(arr[1][1],arr[2][1],arr[5][1]) <= arr[7][1] <= max(arr[8][1],arr[11][1]):
            return True
#    elif min(arr[2][0],arr[3][0]) <= arr[4][0] <= max(arr[5][0],arr[6][0]) and min(arr[1][1],arr[2][1],arr[5][1]) <= arr[4][1] <= max(arr[8][1],arr[11][1]):
#        return True
#    elif min(arr[2][0],arr[3][0]) <= arr[7][0] <= max(arr[5][0],arr[6][0]) and min(arr[1][1],arr[2][1],arr[5][1]) <= arr[7][1] <= max(arr[8][1],arr[11][1]):
#        return True
    else:
        return False

def hot_swap_zone(arr):
    if arr[4][1] >= arr[2][1] or arr[7][1] >= arr[5][1]:
        return True


def judge_pose(arr,index):
    if close_peer(arr,[[3,7]],limitation=1.5) or close_peer(arr,[[4,6]],limitation=1.5) or \
        close_peer(arr,[[4,6],[3,7]],limitation=1.5):
            return 'cold arms'
    elif close_peer(arr,[[4,0]],limitation=1.5) or close_peer(arr,[[7,0]],limitation=1.5):
        return 'hot head'
    elif hot_shirt_zone(arr):
        originalArr = arr
        pass
        return ''
    elif hot_swap_zone(arr):
        originalArr = arr
        pass
        return 'hot_hand_swap'
    elif slope_judge(arr[8],arr[9],arr[10]) != slope_judge(arr[11],arr[12],arr[13]):
        originalArr = arr
        pass
        return 'cold_stomping'
    else:
        return None
'''
cold:
    double arms  single arms Done
        close_peer  3  7      4  6 or both     4  7  1
        
        
    feet shaking action slope
hot:
    T-shirt
        close_peer 4 1  or  7  1 only single and handshaking
        
    head  done Done
        close_peer()  4 0     7  0
    hand shake
        4 y >= 2 y   7 y >= 5 y   handshaking
    
    handshaking  
    original XY    current XY
    r  R
'''

root_path = r'c:\openpose-master'
command = r'windows\x64\Release\OpenPoseDemo.exe -image_dir examples\action -write_keypoint_json examples/action_out -no_display -render_threshold 0.3 -write_images examples/img_data'
img_path = r'c:\openpose-master\examples\action'
json_path = r'C:\python_openpose_project\choosen_ones\hot\action_2'
json_arr = []

#def posture_decode(arr):
#    relative_length = 0
#    if arr[3,2] > 0.5 and arr[4,2] > 0.5:
#        relative_length = eura_distance(arr[3],arr[4])
#    elif arr[6,2] > 0.5 and arr[7,2] > 0.5:
#        relative_length = eura_distance(arr[6],arr[7])
#    # print(relative_length,'relative')
#    # print(math.sqrt(pow(abs(arr[4, 0] - arr[6, 0]), 2) + pow(abs(arr[4, 1] - arr[6, 1]), 2)),'1')
#    # print(math.sqrt(pow(abs(arr[7, 0] - arr[3, 0]), 2) + pow(abs(arr[7, 1] - arr[3, 1]), 2)) ,'2')
#    # print(math.sqrt(pow(abs(arr[4, 0] - arr[0, 0]), 2) + pow(abs(arr[4, 1] - arr[0, 1]), 2)),'3')
#    # print(math.sqrt(pow(abs(arr[7, 0] - arr[0, 0]), 2) + pow(abs(arr[7, 1] - arr[0, 1]), 2)),'4')
#    if relative_length != 0:
#        if eura_distance(arr[4],arr[6]) < relative_length/1.5 or eura_distance(arr[7],arr[3]) < relative_length/1.5:
#            return 'cold'
#        elif eura_distance(arr[4],arr[0]) < relative_length/1.5 or eura_distance(arr[7],arr[0]) < relative_length/1.5:
#            return 'hot'
#    else:
#        return ('not clear for analysing')

get_all_json(json_path,json_arr)
origin_arr = []
index = 0
for i in range(len(json_arr)):#
#    decode_arr(i)
#    print arr
    arr = decode_arr(json_arr[i])
#    print len(arr)
    if len(arr) == 0:
        continue
    elif len(arr) == 18:
#        print arr
        origin_arr = arr
        index = i
        break
#        slope_judge(arr[8],arr[9],arr[10])
#        slope_judge(arr[11],arr[12],arr[13])
#        if hot_shirt_zone(arr):
#            print 'hot_shirt'
#        print close_peer(arr,[[4,1]],limitation=1.5),'\n'
#        print close_peer(arr,[[7,1]],limitation=1.5),'\n'
            
    else:
        for x in arr:
#            print arr
            origin_arr = x
            index = i
            break
#            slope_judge(i[8],i[9],i[10])
#            slope_judge(i[11],i[12],i[13])
#            if hot_shirt_zone(i):
#                print 'hot_shirt'
#            print close_peer(i,[[4,1]],limitation=1.5),'\n'
#            print close_peer(i,[[7,1]],limitation=1.5),'\n'
for i in range(index+1,len(json_arr)):
    arr = decode_arr(json_arr[i])
    if len(arr) == 0:
        continue
    elif len(arr) == 18:
        print handshaking(origin_arr,arr)
    else:
        for i in arr:
            print handshaking(origin_arr,i)
#print(posture_decode(arr))