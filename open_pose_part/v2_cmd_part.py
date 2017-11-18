# -*- coding: utf-8 -*-
"""
Created on Fri Nov 03 08:53:46 2017

@author: User
"""

import os

root_path = r'c:\openpose-master'
'''
 -no_display
 --logging_level 255 no message
'''
command = r'windows\x64\Release\OpenPoseDemo.exe -write_keypoint_json examples/v2_json -render_threshold 0.1 -write_images examples/img_data -frame_rotate 270'
img_json_path = r'c:\openpose-master\examples\v2_json'


def runCMD(path,command):
    originalPath = os.getcwd()
    os.chdir(path)
    os.system(command)
    os.chdir(originalPath)
    
if __name__ == '__main__':
    runCMD(root_path,command)