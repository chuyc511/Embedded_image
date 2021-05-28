import numpy as np
import cv2
B = 255
G = 0
R = 0
n = 0
count = 0
img  = cv2.imread("pointer.PNG")
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#blurred = cv2.GaussianBlur(gray, (5, 5), 0)
canny = cv2.Canny(gray, 30, 150)
cv2.imshow("canny",canny)
ret,markerImag = cv2.threshold(gray,10,255,cv2.THRESH_BINARY_INV)
contours, hierarchy = cv2.findContours(canny,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
print("contours=>"+str(len(contours)))
for c in range(len(contours)):
    if 130>len(contours[c])>120:
        print(len(contours[c]))
        cv2.drawContours(img, contours, c, (B-n,G,R+n), 1)
        n = n + 255
        count = count + 1
        '''
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(img, (x, y), (x+w, y+h), (B+n,G+n,R+n), 1, cv2.LINE_AA)
        '''
    
cv2.imshow("meter",img)
#cv2.imshow("gray",gray)
#cv2.imshow("markerImag",markerImag)
while True :
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()