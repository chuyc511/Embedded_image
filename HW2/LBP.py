# coding=utf-8
from cv2 import cv2
import numpy as np

def origin_LBP(img):
    dst = np.zeros(img.shape,dtype=img.dtype)
    h,w=img.shape
    start_index=1
    for i in range(start_index,h-1):
        for j in range(start_index,w-1):
            print(j)
            center = img[i][j]
            code = 0
#             顺时针，左上角开始的8个像素点与中心点比较，大于等于的为1，小于的为0，最后组成8位2进制
            code |= (img[i-1][j-1] >= center) << (np.uint8)(7)  
            code |= (img[i-1][j  ] >= center) << (np.uint8)(6)  
            code |= (img[i-1][j+1] >= center) << (np.uint8)(5)  
            code |= (img[i  ][j+1] >= center) << (np.uint8)(4)  
            code |= (img[i+1][j+1] >= center) << (np.uint8)(3)  
            code |= (img[i+1][j  ] >= center) << (np.uint8)(2)  
            code |= (img[i+1][j-1] >= center) << (np.uint8)(1)  
            code |= (img[i  ][j-1] >= center) << (np.uint8)(0)  
            dst[i-start_index][j-start_index]= code
    return dst
# 读入灰度图
gray = cv2.imread("./LBP.jpeg", 0)
# LBP处理
org_lbp = origin_LBP(gray)
cv2.imshow('img', gray)
cv2.imshow('org_lbp', org_lbp)
# 若针对视频取图片，delay=k时表示下一帧在kms后选取
cv2.waitKey(0)