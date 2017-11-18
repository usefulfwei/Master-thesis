# -*- coding: utf-8 -*-

# author:Lichang

import os
import json
import numpy as np
import time

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


# new_arr = np.array(new_dict["people"][0]["pose_keypoints"],dtype=np.float32).reshape((18,3))

def changName(originalName):
    return originalName+'_keypoints.json'

def changSerialName(originalName, interval = 1):
    arr = originalName.split('_')
    length = len(arr[1])
    num = int(arr[1])
    num+=interval
    newStr = '0'*(length - len(str(num)))
    arr[1] = newStr+str(num)
    return '_'.join(arr)

def fileName():
    num = int(time.time())
    return str(num)+'_'+'images'

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

json_list = get_all_json(r'C:\Users\Lichang\Documents\Leetcode\python_openpose_project\data',[])[:3]
# data = []
# for i in json_list:
#     data.append(decode_arr(i))
# print(data,'data')
###################################################################

def search_file(start_dir, target):
    os.chdir(start_dir)
    for each_file in os.listdir(os.curdir):
        ext = os.path.splitext(each_file)[1]
        if ext in target:
            vedio_list.append(os.getcwd() + os.sep + each_file + os.linesep)
        if os.path.isdir(each_file):
            search_file(each_file, target)  # 递归调用
            os.chdir(os.pardir)  # 递归调用后切记返回上一层目录


# start_dir = input('请输入待查找的初始目录：')
# program_dir = os.getcwd()
#
# target = ['.mp4', '.avi', '.rmvb']
# vedio_list = []
#
# search_file(start_dir, target)
#
# f = open(program_dir + os.sep + 'vedioList.txt', 'w')
# f.writelines(vedio_list)
# f.close()

#############################################################

# import os
# import os.path
# """获取指定目录及其子目录下的 py 文件路径说明：l 用于存储找到的 py 文件路径 get_py 函数，递归查找并存储 py 文件路径于 l"""
# l = []
# def get_py(path,l):
#     fileList = os.listdir(path)   #获取path目录下所有文件
#     for filename in fileList:
#         pathTmp = os.path.join(path,filename)   #获取path与filename组合后的路径
#         if os.path.isdir(pathTmp):   #如果是目录
#             get_py(pathTmp,l)        #则递归查找
#         elif filename[-3:].upper()=='.PY':   #不是目录,则比较后缀名
#             l.append(pathTmp)
# path = input('请输入路径:').strip()
# get_py(path,l)
# print('在%s目录及其子目录下找到%d个py文件\n分别为：\n'%(path,len(l)))
# for filepath in l:
#     print(filepath+'\n')