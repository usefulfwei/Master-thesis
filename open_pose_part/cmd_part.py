# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 18:41:35 2017

@author: User
"""

import os

def runCMD(path,command):
    originalPath = os.getcwd()
    os.chdir(path)
    os.system(command)
    os.chdir(originalPath)
    

if __name__ == '__main__':
    path = 'c:\openpose-master'
    command = r'windows\x64\Release\OpenPoseDemo.exe -write_keypoint_json examples/media_out'
    runCMD(path,command)
