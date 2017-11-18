# -*- coding: utf-8 -*-
from PIL import Image
import os

path = 'd:/videos'
fileList = os.listdir(path)
for filename in fileList:
    pathTmp = os.path.join(path,filename)
    if 'video4' in pathTmp:
        img = Image.open(pathTmp)
        area = (160, 40, 480, 280)
        cropped_img = img.crop(area)
        print('saving a picture')
        cropped_img.save(filename)
    else:
        continue
