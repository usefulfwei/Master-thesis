# -*- coding: utf-8 -*-

import cv2
vc = cv2.VideoCapture('2.avi')
c=1
if vc.isOpened():
    rval , frame = vc.read()
else:
    rval = False
    timeF = 1000
while rval:
    rval, frame = vc.read()
    if(c%timeF == 0):
        cv2.imwrite('image/'+str(c) + '.jpg',frame)
    c = c + 1
    cv2.waitKey(1)
vc.release()