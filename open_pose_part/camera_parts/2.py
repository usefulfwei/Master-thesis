# -*- coding: utf-8 -*-

# author:Lichang

import VideoCapture
import time
cap = VideoCapture.Device(devnum=0,showVideoWindow=0)


def quick_snap():
    time.sleep(0.1)
    pic_name = int(time.time()*10)
    cap.getImage(timestamp=1).save(str(pic_name) + '.jpg')

while True:
    time.sleep(10)
    pic_name = int(time.time()*10)
    cap.getImage(timestamp=1).save(str(pic_name)+'.jpg')
    # # 效果并不好
    # strR = input()
    # if strR == 'q' or strR == 'Q':
    #     break


#saveSnapshot

