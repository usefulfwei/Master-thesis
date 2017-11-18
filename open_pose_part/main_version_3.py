# -*- coding: utf-8 -*-

# author:Lichang

# -*- coding: utf-8 -*-
"""
Created on Fri Nov 03 08:16:53 2017

@author: User
"""

import os
# from Tkinter import *
# import VideoCapture
import msvcrt
import json
import numpy as np
# import time
import math
import multiprocessing as mp


def runCMD(path, command):
    originalPath = os.getcwd()
    os.chdir(path)
    os.system(command)
    os.chdir(originalPath)


def get_all_json(path, json_arr):
    fileList = os.listdir(path)
    for filename in fileList:
        pathTmp = os.path.join(path, filename)
        if os.path.isdir(pathTmp):
            get_all_json(pathTmp, json_arr)
        elif filename[-5:].upper() == '.JSON':
            json_arr.append(pathTmp)
        else:
            continue


def decode_arr(path):
    if os.access(path, os.F_OK):
        with open(path) as f:
            try:
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
            except:
                return []


def eura_distance(arr1, arr2):
    return math.sqrt(pow(abs(arr1[0] - arr2[0]), 2) + pow(abs(arr1[1] - arr2[1]), 2))


def close_peer(array, peer, limitation=1.5):
    relative_length = 0
    if array[3, 2] > 0.5 and array[4, 2] > 0.5:
        relative_length = eura_distance(array[3], array[4])
    elif array[6, 2] > 0.5 and array[7, 2] > 0.5:
        relative_length = eura_distance(array[6], array[7])
    if relative_length != 0:
        for i in peer:
            p1 = i[0]
            p2 = i[1]
            if eura_distance(array[p1], array[p2]) > relative_length / limitation or \
                            array[p1][0] == array[p2][0] or array[p1][1] == array[p2][1]:
                return None
        else:
            return True
    else:
        return None


def slope_judge(arr1, arr2=[], difference=30.0):
    def _slope_judge(arr1, arr2, arr3):
        if int(arr1[0]) == 0 or int(arr2[0]) == 0 or int(arr3[0]) == 0:
            return None
        else:
            slope1 = float(arr1[1] - arr2[1]) / (arr1[0] - arr2[0])
            slope2 = float(arr2[1] - arr3[1]) / (arr2[0] - arr3[0])
            if abs(slope1 - slope2) < difference:
                return 'straight'
            else:
                return 'bending'

    if arr2 == []:
        if _slope_judge(arr1[8], arr1[9], arr1[10]) is not None and _slope_judge(arr1[11], arr1[12],
                                                                                 arr1[13]) is not None and \
                (_slope_judge(arr1[8], arr1[9], arr1[10]) != _slope_judge(arr1[11], arr1[12], arr1[13])):
            return True
        else:
            return False
    else:
        if _slope_judge(arr1[8], arr1[9], arr1[10]) != _slope_judge(arr2[8], arr2[9], arr2[10]) or \
                        _slope_judge(arr1[11], arr1[12], arr1[13]) != _slope_judge(arr2[11], arr2[12], arr2[13]):
            return True
        else:
            return False


def handshaking(arr1, arr2, r_min=2.0, r_max=120.0):
    if r_min <= eura_distance(arr1[4], arr2[4]) <= r_max or r_min <= eura_distance(arr1[7], arr2[7]) <= r_max:
        return True
    else:
        return False


def hot_shirt_zone(arr):
    relative_length = eura_distance(arr[2], arr[5])
    if max(arr[2][0], arr[3][0]) < arr[4][0] < min(arr[5][0], arr[6][0]) and eura_distance(arr[4],
                                                                                           arr[1]) < relative_length or \
                                    max(arr[2][0], arr[3][0]) < arr[7][0] < min(arr[5][0], arr[6][0]) and eura_distance(
                arr[7], arr[1]) < relative_length:
        return True
    else:
        return False


def hot_swap_zone(arr):
    if (arr[4][1] < arr[2][1] and arr[3][0] < arr[4][0] < arr[1][0]) or \
            (arr[7][1] < arr[5][1] and arr[1][0] < arr[7][0] < arr[6][0]):
        return True
    else:
        return False


def judge_pose(arr, json_arr):
    if close_peer(arr, [[3, 7]], limitation=2.0) or close_peer(arr, [[4, 6]], limitation=2.0):
        return 'cold arms'
    elif close_peer(arr, [[4, 16]], limitation=2.0) or close_peer(arr, [[7, 17]], limitation=2.0):
        return 'hot head'
    elif slope_judge(arr):
        originalArr = arr
        start_idx = 0 if len(json_arr) < 30 else len(json_arr) - 30
        count = 0
        for i in range(start_idx, len(json_arr) - 1):
            arr = decode_arr(json_arr[i])
            if arr is None or len(arr) == 0:
                continue
            elif len(arr) == 18:
                if slope_judge(originalArr, arr):
                    originalArr = arr
                    count += 1
                    continue
            else:
                for i in arr:
                    if slope_judge(originalArr, i):
                        originalArr = i
                        count += 1
                        continue
        if count >= (len(json_arr) - start_idx) // 4:
            return 'cold_stomping_action'
        else:
            print
            'duojiao fail'
            return 'Cannot figure the posture'
    elif hot_swap_zone(arr):
        originalArr = arr
        count = 0
        start_idx = 0 if len(json_arr) < 30 else len(json_arr) - 30
        for i in range(start_idx, len(json_arr) - 1):
            arr = decode_arr(json_arr[i])
            if arr is None or len(arr) == 0:
                continue
            elif len(arr) == 18:
                if handshaking(originalArr, arr):
                    count += 1
                    originalArr = arr
                    continue
            else:
                for i in arr:
                    if handshaking(originalArr, i):
                        count += 1
                        originalArr = i
                        continue
        if count >= (len(json_arr) - start_idx) // 4:
            return 'hot_hand_swap'
        else:
            print
            'shanfeng fail'
            return 'Cannot figure the posture'
    elif hot_shirt_zone(arr):
        originalArr = arr
        start_idx = 0 if len(json_arr) < 30 else len(json_arr) - 30
        count = 0
        for i in range(start_idx, len(json_arr) - 1):
            arr = decode_arr(json_arr[i])
            if arr is None or len(arr) == 0:
                continue
            elif len(arr) == 18:
                if handshaking(originalArr, arr):
                    count += 1
                    originalArr = arr
                    continue
            else:
                for i in arr:
                    if handshaking(originalArr, i):
                        count += 1
                        originalArr = i
                        continue
        if count >= (len(json_arr) - start_idx) // 4:
            return 'hot_shirt_action'
        else:
            print
            ' fail shirt'
            return 'Cannot figure the posture'
    else:
        print
        'cannot goes into action'
        return 'Cannot figure the posture'


# def deleteImg(imgPath):
#    originalPath = os.getcwd()
#    os.chdir(imgPath)
#    fileList = os.listdir(imgPath)
#    for filename in fileList:
#        pathTmp = os.path.join(imgPath,filename)
#        os.remove(pathTmp)
#    os.chdir(originalPath)

def deleteJson(json_arr):
    for i in json_arr:
        os.remove(i)


def start_cleaning(arr):
    originalPath = os.getcwd()
    for i in arr:
        os.chdir(i)
        fileList = os.listdir(i)
        for fileName in fileList:
            pathTmp = os.path.join(i, fileName)
            os.remove(pathTmp)
    os.chdir(originalPath)


root_path = r'c:\openpose-master'
'''
 -no_display
 --logging_level 255 no message
'''
command = r'windows\x64\Release\OpenPoseDemo.exe -write_keypoint_json examples/v2_json -write_images examples/img_data --logging_level 255'
root_command = r'c:\openpose-master\windows\x64\Release\OpenPoseDemo.exe -write_keypoint_json examples/v2_json -render_threshold 0.1 -write_images examples/img_data -process_real_time'
img_json_path = r'c:\openpose-master\examples\v2_json'


# def openpose_job():
#     runCMD(root_path, command)


#    os.system(command)

# def analysis_job(textEle):
#     json_arr = []
#     while True:
#         get_all_json(img_json_path, json_arr)
#         arr = decode_arr(json_arr[-1]) if len(json_arr) > 0 else None
#         if arr is None or len(arr) == 0:
#             continue
#         elif len(arr) == 18:
#             if judge_pose(arr, json_arr) != 'Cannot figure the posture':
#                 textEle.set(judge_pose(arr, json_arr))
#         else:
#             for i in arr:
#                 if judge_pose(i, json_arr) != 'Cannot figure the posture':
#                     textEle.set(judge_pose(arr, json_arr))
#                     break
#         if len(json_arr) < 100:
#             continue
#         else:
#             try:
#                 deleteJson(json_arr)
#             except:
#                 continue
#             json_arr = []

#
# def quit_job():
#     print('enter q to quit')
#
#     while True:
#         if ord(msvcrt.getch()) in [81, 113]:
#             break
#
#     print('goes out')


from tkinter import *


class App:
    def __init__(self, master):
        self.frame = Frame(master,height=100,width=350)
        self.b = Button(self.frame, text='OpenCamera', command=self.openFile)
        self.c = Button(self.frame, text='OpenAnalysis', command=self.openProcess)
        self.d = Button(self.frame, text='OpenUnderstanding', command=self.openAnalysis)
        self.var1 = StringVar()
        self.e = Label(self.frame,textvariable=self.var1)
        self.b.grid(row=1, column=0)
        self.c.grid(row=1, column=1)
        self.d.grid(row=1, column=2)
        self.e.grid(row=1, column=3)
        self.frame.grid()

    def openFile(self):
        os.startfile(r'C:\Program Files (x86)\Noël Danjou\AMCap\amcap.exe')

    def openProcess(self):
        runCMD(root_path, command)
    def openAnalysis(self):
        json_arr = []
        while True:
            get_all_json(img_json_path, json_arr)
            arr = decode_arr(json_arr[-1]) if len(json_arr) > 0 else None
            if arr is None or len(arr) == 0:
                continue
            elif len(arr) == 18:
                if judge_pose(arr, json_arr) != 'Cannot figure the posture':
                    self.var1.set(judge_pose(arr, json_arr))
            else:
                for i in arr:
                    if judge_pose(i, json_arr) != 'Cannot figure the posture':
                        self.var1.set(judge_pose(arr, json_arr))
                        break
            if len(json_arr) < 100:
                continue
            else:
                try:
                    deleteJson(json_arr)
                except:
                    continue
                json_arr = []


if __name__ == '__main__':
    start_cleaning([img_json_path])
    root = Tk()
    root.title('my window')
    root.geometry('500x100')

    app = App(root)
    root.mainloop()
