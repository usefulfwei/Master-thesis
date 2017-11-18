# -*- coding: utf-8 -*-

# author:Lichang


import numpy as np
import cv2
import time
cap = cv2.VideoCapture('test.avi')
count = 0

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        count += 1
        cv2.imshow('frame', frame[:, 670:1200])
    if cv2.waitKey(1) & 0xFF == ord('q') & ret == False:
        break
print(count)
cap.release()
cv2.destroyAllWindows()