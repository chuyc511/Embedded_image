import cv2
import numpy as np
img = cv2.imread('meter2.PNG')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('original', img)
gaussian = cv2.GaussianBlur(gray, (3, 3), 0)
circles1 = cv2.HoughCircles(gaussian, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=30, minRadius=15, maxRadius=80)
print(np.shape(circles1))             # hough_gradient 霍夫梯度法
circles = circles1[0, :, :]
circles = np.uint16(np.around(circles))
for i in circles[:]:
    cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 3)
    cv2.circle(img, (i[0], i[1]), 2, (255, 0, 255), 10)
cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()