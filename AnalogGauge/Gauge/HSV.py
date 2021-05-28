import cv2
import numpy as np
import math
img = cv2.imread("meter2P.PNG")
img = cv2.resize(img, (400, 200), interpolation=cv2.INTER_CUBIC)
gray =  cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
redLower = np.array([156, 43, 46])
redUpper = np.array([179, 255, 255])
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


mask = cv2.inRange(hsv, redLower, redUpper)
cv2.imshow('mask', mask)


edges = cv2.Canny(gray, 50, 200)
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 30)
for x1,y1,x2,y2 in lines[0]:
    print(lines[0])
    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
#cv2.line(img, (int(x1/count), int(y1/count)), (int(x2/count), int(y2/count)), (0, 0, 255), 1)
    
    
cv2.imshow('Canny', edges)
#kernel = np.ones((5, 5), np.uint8)
#dilation = cv2.dilate(binary, kernel, iterations=1)


contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
if len(contours) > 0:
    boxes = [cv2.boundingRect(c) for c in contours]
    for box in boxes:
        x, y, w, h = box
        #cv2.rectangle(img, (x, y), (x+w, y+h), (153, 153, 0), 2)
        
        
        
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()