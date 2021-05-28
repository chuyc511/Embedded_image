import cv2
import numpy as np
img = cv2.imread("meterP.PNG")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
canny = cv2.Canny(gray, 50, 200)
B = 0
G = 0
R = 0
n = 0
r = 8
h = w = r * 2 + 1
kernel = np.zeros((h, w), dtype=np.uint8)
cv2.circle(kernel, (r, r), r, 1, -1)   
openingimg = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
ret,markerImag = cv2.threshold(openingimg,50,255,cv2.THRESH_BINARY_INV)

contours, hierarchy = cv2.findContours(markerImag,cv2.cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
print(len(contours))
clone = img.copy()
clone2 = img.copy()
area=[]
for c in contours:
    area.append(cv2.contourArea(c))
max_area = np.argmax(np.array(area))
cv2.drawContours(clone2, contours, max_area, (0, 255, 0), cv2.FILLED)
#cv2.fillPoly(clone2, max_area, (0,0,255))
"""
for c in contours:
    (x, y, w, h) = cv2.boundingRect(c)
    cv2.rectangle(clone, (x, y), (x + w, y + h), (0, 255, 0), 2)
"""    
"""
for c in contours:
    if len(c)>100:
        cv2.drawContours(clone, c, -1, (0, 255, 0), 2)
"""
cv2.imshow('openingimg', openingimg)
cv2.imshow('markerImag', markerImag)
cv2.imshow('img', img)
cv2.imshow('clone2', clone2)

cv2.waitKey(0)
cv2.destroyAllWindows()