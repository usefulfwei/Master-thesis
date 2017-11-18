# -*- coding: utf-8 -*-

import numpy as np
import cv2
import datetime

cap = cv2.VideoCapture(1)
cap.set(3, 1920)
cap.set(4, 1080)
# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('test.avi',fourcc, 20.0, (1280,1080))
i = datetime.datetime.now()
name = str(i.year) + '_' + str(i.month) + '_' + str(i.day) + '-' + str(i.hour) + '_' + str(
    i.minute) + '_' + str(i.second)
out = cv2.VideoWriter(name + '.avi',fourcc, 30.0,(1920,1080))

while(cap.isOpened()):
    ret, frame = cap.read()

    if ret==True:
        frame = cv2.flip(frame,180)
        # write the flipped frame
        out.write(frame)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()