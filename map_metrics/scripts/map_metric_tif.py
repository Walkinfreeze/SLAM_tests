#!/usr/bin/env python
import re
import numpy as np

import os
from os import listdir
from os.path import isfile,join
import csv
import sys
import cv2 as cv
from matplotlib import pyplot as plt
import datetime
import shutil

datetime_object = datetime.datetime.now()

np.set_printoptions(threshold=1000)

numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

#assign working directory to variable
file_path=os.getcwd()
file_path=os.path.normpath(os.getcwd() + os.sep + os.pardir+'/'+'hector_ws'+'/'+'src'+'/'+'hector_slam'+'/'+'hector_geotiff'+'/'+'maps')
#print(file_path)
#setting path for data folder
data_path=file_path

# extracting file names with extensions
full_file_names=[f for f in listdir(data_path) if f.endswith('.tif')]
full_file_names=sorted(full_file_names, key=numericalSort)
#checking file names and extensions

#print(full_file_names)
#print('\n')

if __name__ == "__main__":
    from PIL import Image
    occupied_=[0 for m in range(len(full_file_names))]
    free_=[0 for n in range(len(full_file_names))]
    total_=[0 for o in range(len(full_file_names))]
    for k in range(len(full_file_names)):
#       image = read_pgm(full_file_names[k], byteorder='<')
#        image = Image.open(file_path+'/'+full_file_names[k])
#        imarray = numpy.array(image)

        img = cv.imread(file_path+'/'+full_file_names[k],0)
        ret,img_bin = cv.threshold(img,127,255,cv.THRESH_BINARY)
	
        #print(img.shape)

#        titles = ['Original Image','BINARY']
#        images = [img, img_bin]
#        for i in xrange(2):
#            plt.subplot(2,1,i+1),plt.imshow(images[i],'gray')
#            plt.title(titles[i])
#            plt.xticks([]),plt.yticks([])
#        plt.show()
        for i in range(img_bin.shape[0]):
           for j in range(img_bin.shape[1]):
              if img_bin[i,j] == 0:
                  occupied_[k] += 1
              else:
                 free_[k]  += 1
	total_[k] = occupied_[k] + free_[k]


occupied_np_ = np.array(occupied_, dtype=np.float)
free_np_ = np.array(free_, dtype=np.float)
total_np_ = np.array(total_, dtype=np.float)
occupied_pct_ = (occupied_np_ / total_np_)*100
free_pct_ = (free_np_ / total_np_)*100
#print('percentage occupied pixels = ' + str(occupied_pct_)+'\n')
#print('percentage free pixels = ' + str(free_pct_)+'\n')
#print('total amount of pixels = ' + str(total_np_[0])+'\n')

# x axis values 
x_ = range(len(full_file_names)) 
# corresponding y axis values 
y_occupied_ = occupied_
y_free_ = free_

  
# plotting the points  

fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle('Amount of Pixels Occupied/Free')
ax1.plot(x_, y_occupied_, 'r', marker='.') 
ax1.set_ylabel('occupied pixels')
ax1.set_xlabel('map_files')
ax1.grid() 
ax2.plot(x_, y_free_, 'g', marker='.')
ax2.set_xlabel('map files')
ax2.set_ylabel('free pixels')
ax2.grid()

my_path = os.path.normpath(os.getcwd() + os.sep + os.pardir+'/'+'hector_ws'+'/'+'src'+'/'+'map_metrics'+'/'+'figures')
my_file = str(datetime_object) +'.png'
fig.savefig(os.path.join(my_path, my_file)) 

#for r in range(len(full_file_names)):
#    map_file = file_path +'/'+str(full_file_names[r])
#    map_destination = os.path.normpath(os.getcwd() + os.sep + os.pardir+'/'+'hector_ws'+'/'+'figures'+'/'+'maps')+'/'+str(full_file_names[r])
#    shutil.move(map_file,map_destination)

  
# function to show the plot 
#plt.show()
