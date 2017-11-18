# -*- coding: utf-8 -*-

# author:Lichang

import serial
import time

ser = serial.Serial('COM4', 9600)
line = ser.readline()
with open('temperature.txt','w') as f:
    while line:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        f.write('\t')
        f.write(str(line[:-1])[2:6])
        f.write('\n')
        time.sleep(1)
        line = ser.readline()
f.close()
ser.close()