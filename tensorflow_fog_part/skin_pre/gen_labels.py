# -*- coding: utf-8 -*-

# author:Lichang

import xlrd
import numpy as np
import os

class Temp:
    def __init__(self):
        self.labels = []
T_info = []

temp_arr = []
form_path = r'./form/'

for file in os.listdir(form_path):
    pathTmp = os.path.join(form_path+file)
    workbook = xlrd.open_workbook(pathTmp)
    sheet = workbook.sheet_by_index(0)
    result = [pathTmp]
    for row in range(2,sheet.nrows):
        print(sheet.cell(row,1).value)
        result.append(sheet.cell(row,1).value)
    print(result)
    temp_arr.append(result)

print(len(temp_arr))
for arr in temp_arr:
    temp = []
    for i in range(1,len(arr)-1):
        temp.append(arr[i])
        gap = round((arr[i+1] - arr[i]) / 11,4)
        for j in range(11):
            temp.append(arr[i] + gap)
    temp.append(arr[len(arr)-1])
    print(len(temp))
    T_info.append({arr[0]:temp})

# arr = temp_arr[0]
# temp = []
# for i in range(1,len(arr)-1):
#     temp.append(arr[i])
#     gap = (arr[i+1] - arr[i]) / 11
#     for j in range(11):
#         temp.append(arr[i] + gap)
# temp.append(arr[len(arr)-1])
# print(len(temp),'length')
# print(temp)
