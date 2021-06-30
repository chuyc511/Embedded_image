import cv2
import numpy as np
import os
from angle import math_angle
from Perspective import Transform

class Gauge() :
    def Gauge_Reader(Min_Value, Max_Value, Min_Angle, Max_Angle,CenterX, CenterY):
        print(Min_Value, Max_Value, Min_Angle, Max_Angle,CenterX, CenterY)
        cap = cv2.VideoCapture(0)

        while cap.isOpened() :
          try :
            ret, frame = cap.read()
            image_org = Transform.Trans(frame)
            cv2.imshow('tran', image_org)

            try :
                img_hsv = cv2.cvtColor(image_org,cv2.COLOR_BGR2HSV)
                rows, cols, channels = image_org.shape
                # 区间1
                lower_red = np.array([0, 43, 46])
                upper_red = np.array([60, 255, 255])
                mask0 = cv2.inRange(img_hsv,lower_red,upper_red)
                # 区间2
                lower_red = np.array([130, 43, 46])
                upper_red = np.array([255, 200, 200])
                mask1 = cv2.inRange(img_hsv,lower_red,upper_red)
                # 拼接两个区间
                mask = mask0 + mask1       
                kernel = np.ones((3,3), np.uint8)
                mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel,iterations=3) 
                # cv2.imshow('mask', mask)
                exc, cnts, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  
                
                max_contour = max(cnts, key=len)
                rect = cv2.minAreaRect(max_contour)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.drawContours(mask, [box], 0, (255, 255, 0), 3)
                cv2.drawContours(image_org, [box], 0, (255, 255, 0), 3)

                cv2.imshow('mask', mask)
   
                Total_Angle = 0
                print("CenterX, CenterY : ",CenterX,CenterY)
                for i in range(0,len(box)) :  
                    if CenterX - box[i][0] < 0 :
                        Line_Angles = 90 + math_angle.azimuthAngle(0, 0, box[i][0] - CenterX, CenterY - box[i][1])
                    else :
                        Line_Angles = math_angle.azimuthAngle(0, 0, box[i][0] - CenterX, CenterY - box[i][1]) - 270
                    print("box : ", box[i][0], box[i][1])
                    print("reduce : ", box[i][0] - CenterX, CenterY - box[i][1])
                    print("ttttttttt :",Line_Angles)
                    Total_Angle += Line_Angles
                    
                print(Total_Angle/4)    
                
                Current = str(int(Max_Value*(int(Total_Angle/4) - Min_Angle)/(Max_Angle - Min_Angle)))

                cv2.putText(image_org, '%s%s' %(Current,"A"), (int(CenterX),int(CenterY)), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2,cv2.LINE_AA)

                cv2.line(image_org, (CenterX,0), (CenterX,CenterY),(0, 255, 0), 2)
                cv2.line(image_org, (CenterX,CenterY), (CenterX,300),(0, 255, 0), 2)
                cv2.line(image_org, (0,CenterY), (CenterX,CenterY),(255, 0, 0), 2)
                cv2.line(image_org, (CenterX,CenterY), (300,CenterY),(255, 0, 0), 2)
                   
                cv2.imshow('image_org', image_org)
                
            except :
                cv2.imshow('image_org', frame)
   
          except :
             pass
          if cv2.waitKey(1) & 0xFF == ord('q'):  
             break


        cv2.destroyAllWindows()
        cap.release()
        
if __name__ == "__main__":
    Gauge.Gauge_Reader(0,100,46,109,146,210)
