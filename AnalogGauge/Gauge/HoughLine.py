import cv2
import numpy as np
import math
img = cv2.imread('meter2P.PNG')
img = cv2.resize(img, (400, 200), interpolation=cv2.INTER_CUBIC)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 200)
lines = cv2.HoughLines(edges, 1, np.pi/180, 120)

print(np.shape(lines))
lines = lines[:, 0, :]
for rho, theta in lines:
    print("theta : "+str(theta))
    print("rho : "+str(rho))
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*a)
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*a)
    slope=(y2-y1)/(x2-x1)
    print("slope : "+str(math.degrees(math.atan(slope))))
    cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
'''
for x1,y1,x2,y2 in lines[0]:
    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
    '''
cv2.imshow('img', img)
cv2.imshow('edges', edges)
cv2.waitKey(0)
cv2.destroyAllWindows()