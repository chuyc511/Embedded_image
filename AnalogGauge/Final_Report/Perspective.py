import cv2
import numpy as np


class Transform() :
    
    def Trans(frame) :
        xax=[0]*2
        yax=[0]*2
        final=[0]*4
        pts1 = np.float32([[56,65],[368,52],[28,387],[389,390]])
        pts2 = np.float32([[0,0],[0,300],[300,0],[300,300]])
           
        img2 = frame.copy()
        img = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)    
        ret, th1 = cv2.threshold(img, 140, 225, cv2.THRESH_BINARY)
        kernel = np.ones((5,5), np.uint8)
        kernel2 = np.ones((5,5), np.uint8)
        
        erosion = cv2.erode(th1, kernel, iterations =1)
        dilation = cv2.dilate(erosion, kernel2, iterations =1)

        blurred = cv2.GaussianBlur(dilation, (5, 5), 0)
        #cv2.imshow("blurred",blurred) 
        #cv2.waitkey()
        #cv2.destroyAllWindows()

     
        (excep, cnts, _) = cv2.findContours(blurred.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        clone = img2.copy()
        
        try:
            max_contour = max(cnts, key=len)
            x, y, w, h = cv2.boundingRect(max_contour)   
            box = cv2.minAreaRect(max_contour)
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
            epsilon =1*cv2.arcLength(max_contour,True)
            peri = cv2.arcLength(max_contour, True)

            approx = cv2.approxPolyDP(max_contour, 0.08 * peri, True)     
            if len(approx)==4:
                cv2.drawContours(frame,[approx],0,(255,0,0),2)
                sort=sorted(approx.tolist(),key= lambda x:x[0])
                xax[0]=(sort[0]) 
                xax[1]=(sort[1])
                xax=sorted(xax ,key= lambda x:x[0][1])
                yax[0]=(sort[2]) 
                yax[1]=(sort[3]) 
                yax=sorted(yax ,key= lambda x:x[0][1])
                final[0]=xax[0]
                final[1]=xax[1]
                final[2]=yax[0]
                final[3]=yax[1]
                
                M = cv2.getPerspectiveTransform(np.float32(final), pts2 )
                trs = cv2.warpPerspective(clone,M,(300,300))
                cv2.imwrite("./Save.jpg",trs)
                return trs
              
        except Exception as e:
            print(e)
            Save = cv2.imread("./Save.jpg")

            return Save

