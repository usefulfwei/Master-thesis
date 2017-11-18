# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 08:23:03 2017

@author: User
"""

import os

root_path = r'c:\openpose-master'
command = r'windows\x64\Release\OpenPoseDemo.exe -image_dir examples\action -write_keypoint_json examples/action_out -no_display -render_threshold 0.3'
img_path = r'c:\openpose-master\examples\action'
json_path = r'c:\openpose-master\examples\action_out'


def deleteImg(imgPath):
    originalPath = os.getcwd()
    os.chdir(imgPath)
    fileList = os.listdir(imgPath)
    for filename in fileList:
        pathTmp = os.path.join(imgPath,filename)
        os.remove(pathTmp)
    os.chdir(originalPath)

json_arr = []

def get_all_json(path,json_arr):
    fileList = os.listdir(path)
    for filename in fileList:
        pathTmp = os.path.join(path,filename)
        if os.path.isdir(pathTmp):
            get_all_json(pathTmp,json_arr)
        elif filename[-5:].upper() == '.JSON':
            json_arr.append(pathTmp)
    return json_arr

def deleteJson(json_arr,index=0):
    if index < 0:
        return
    elif index >= len(json_arr):
        index == len(json_arr)
    for i in range(index):
        os.remove(json_arr[i])
    print 'delete success'
        


def runCMD(path,command):
    originalPath = os.getcwd()
    os.chdir(path)
    os.system(command)
    os.chdir(originalPath)

#deleteImg(img_path)
get_all_json(json_path,json_arr)
deleteJson(json_arr,3)