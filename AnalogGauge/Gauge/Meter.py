import cv2
import numpy as np
img = cv2.imread("meter.PNG")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

r = 8
h = w = r * 2 + 1
kernel = np.zeros((h, w), dtype=np.uint8)
cv2.circle(kernel, (r, r), r, 1, -1)

openingimg = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
strtimg = cv2.absdiff(gray, openingimg)
ret,markerImag = cv2.threshold(strtimg,150,255,cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(markerImag,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
for c in range(len(contours)):
        print(len(contours[c]))
        cv2.drawContours(img, contours, c, (0,0,255), 1)

cv2.imshow('img', img)
cv2.imshow('openingimg', openingimg)
cv2.imshow('strtimg', strtimg)
cv2.imshow('markerImag', markerImag)

cv2.waitKey(0)
cv2.destroyAllWindows()