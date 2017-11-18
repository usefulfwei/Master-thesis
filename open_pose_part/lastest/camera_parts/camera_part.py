# -*- coding: utf-8 -*-

# author:Lichang

import VideoCapture
import time
import msvcrt
import os

img_path = r'c:\openpose-master\examples\action'
os.chdir(img_path)
cap = VideoCapture.Device(devnum=0,showVideoWindow=0)

def quick_snap():
    time.sleep(0.1)
    pic_name = int(time.time()*10)
    cap.getImage(timestamp=1).save(str(pic_name) + '.jpg')

while True:
    print 'taking photos'
    time.sleep(0.1)
    pic_name = int(time.time()*10)
    cap.getImage(timestamp=1).save(str(pic_name)+'.jpg')
#    if ord(msvcrt.getch()) in [81,113]:
#        print('program quiting...')
#        break
    # # 效果并不好
    # strR = input()
    # if strR == 'q' or strR == 'Q':
    #     break


#saveSnapshot
