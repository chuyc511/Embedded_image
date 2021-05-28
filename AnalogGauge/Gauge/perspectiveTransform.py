# coding: utf-8
import cv2
import numpy as np
k=0
pts1 = np.float32([[56,65],[368,52],[28,387],[389,390]])
pts2 = np.float32([[0,0],[0,300],[300,0],[300,300]])
img = cv2.imread("pic/G.jpg")
#print img.shape
"""
順序
1---------3
|         |
|         |
|         |
2---------4
"""
def trans():
    M = cv2.getPerspectiveTransform(pts1,pts2)
    trs = cv2.warpPerspective(img,M,(300,300))
    cv2.imshow("img", trs)
    cv2.waitKey(0)    
    return 0
def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    global k
    global pts1
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        print (xy)
        print(k)
        pts1[k]=np.float32([[x,y]])
        k=k+1
        cv2.circle(img, (x, y), 1, (255, 0, 0), thickness = -1)
        cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                    1.0, (0,0,0), thickness = 1)
        cv2.imshow("image", img)

cv2.namedWindow("image")
cv2.imshow("image", img)
cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
while(True):
    try:
       if (k>3):
            cv2.destroyWindow("image")
            trans()
            break
       cv2.waitKey(100)
    except Exception:
        cv2.destroyWindow("image")
        break
print('end')        
cv2.destroyWindow()