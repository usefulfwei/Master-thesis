# -*- coding: utf-8 -*-

import numpy as np
import cv2
import datetime
cap = cv2.VideoCapture(1)
cap.set(3, 1920)
cap.set(4, 1080)
# Define the codec and create VideoWriter object
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# # out = cv2.VideoWriter('test.avi',fourcc, 20.0, (1280,1080))
#
# out = cv2.VideoWriter('test.avi',fourcc, 20.0,(960,720))
count = 0
original_second = None
while(cap.isOpened()):
    ret, frame = cap.read()

    i = datetime.datetime.now()

    if not original_second or original_second != i.second:
        count = 0
        original_second = i.second
    else:
        count += 1
    print(count)
    if ret==True:
        # ret.save(str(time.time())+'')
        frame = cv2.flip(frame,180)

        name = str(i.year) + '_' + str(i.month) + '_' + str(i.day) + '-' + str(i.hour) + '_' + str(i.minute) + '_' + str(i.second) + '_' + str(count) + 'frame'
        print(name)
        cv2.imwrite(str(name)+'.jpg', frame)
        # write the flipped frame
        # out.write(frame)

        cv2.imshow('frame',frame)
        if cv2.waitKey(2) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
# out.release()
cv2.destroyAllWindows()