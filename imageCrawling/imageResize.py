#210515
import os
import cv2
import numpy as np

path='download/'
data_list_back = os.listdir(path)
print(data_list_back)
num=1
try:
    for i in data_list_back:
        img_array = np.fromfile(path+i, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)#img = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)
        #img=cv2.imread('download/'+i)
        img=cv2.resize(img,(150,150))
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('resize_front_150/1_'+str(num)+'.jpg',img)
        num+=1
except Exception as e:
        print(str(e))

'''
path='front_face/'
data_list_back = os.listdir(path)
#print(data_list_back)
num=1
try:
    for i in data_list_back:
        img_array = np.fromfile('front_face/'+i, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        #img=cv2.imread('download/'+i)
        img=cv2.resize(img,(150,150))
        cv2.imwrite('resize_front_150/1_'+str(num)+'.jpg',img)
        num+=1
except Exception as e:
        print(str(e))
        
'''