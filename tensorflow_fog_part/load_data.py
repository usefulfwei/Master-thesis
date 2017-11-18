# -*- coding: utf-8 -*-

# author:Lichang

import numpy as np
import PIL.Image as Image
import pickle
import os

class frogData:
    def __init__(self):
        self.images = np.array([])
        self.labels = np.array([])

# 76800
data_frog = frogData()

original_path = os.getcwd()
frog_path = r'./img/hasfrog/'
no_frog_path = r'./img/nofrog/'
data_base_path = "./data/"
path_arr = [frog_path, no_frog_path]
pic_amount = 0
for path in path_arr:
    for file in os.listdir(path):
        pathTmp = os.path.join(path+file)
        if pathTmp[-4:].upper() == '.JPG':
            pic_amount += 1
            image = Image.open(pathTmp)
            r,g,b = image.split()
            r_arr = np.array(r).reshape(76800)
            g_arr = np.array(g).reshape(76800)
            b_arr = np.array(b).reshape(76800)
            image_arr = np.concatenate((r_arr,g_arr,b_arr))
            data_frog.images = np.concatenate((data_frog.images,image_arr))
            if frog_path in pathTmp:
                data_frog.labels = np.concatenate((data_frog.labels,np.array([1])))
            else:
                data_frog.labels = np.concatenate((data_frog.labels, np.array([0])))

data_frog.images = data_frog.images.reshape((pic_amount,230400))
print(data_frog.images.shape[1],'instance of pics')
print(data_frog.labels.shape[0],'instance of labels')

output = open('data.pkl', 'wb')
filepath = data_base_path+'data.pkl'

with open(filepath,mode='wb') as f:
    pickle.dump(data_base_path,f)

print("保存成功")




