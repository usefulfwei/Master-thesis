# -*- coding: utf-8 -*-

# author:Lichang


import numpy as np
import cv2
import time
cap = cv2.VideoCapture(r'./video/6.avi')
start = time.time()
count = 0
while(cap.isOpened()):
    ret, frame = cap.read()
    count += 1
    if time.time() - start > 2:
        break
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
print(count)
cap.release()
cv2.destroyAllWindows()