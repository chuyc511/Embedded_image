import cv2
import numpy as np
from imutils import contours
import cv2 as cv

def tomygray(image):
    height = image.shape[0]
    width = image.shape[1]
    gray = np.zeros((height, width, 1), np.uint8)
    for i in range(height):
        for j in range(width):
            # pixel = max(image[i,j][0], image[i,j][1], image[i,j][2])
            pixel = 0.0 * image[i, j][0] + 0.0 * image[i, j][1] + 1 * image[i, j][2]
            gray[i, j] = pixel
    return gray

def TubeIdentification(image):
    tube = 0
    tubo_roi = [
         [image.shape[0] * 0/3, image.shape[0] * 1/3, image.shape[1] * 1/2, 
                                                      image.shape[1] * 1/2],
         [image.shape[0] * 1/3, image.shape[0] * 1/3, image.shape[1] * 2/3, 
                                                      image.shape[1] - 1  ],
         [image.shape[0] * 2/3, image.shape[0] * 2/3, image.shape[1] * 2/3, 
                                                      image.shape[1] - 1  ],
         [image.shape[0] * 2/3, image.shape[0] -1   , image.shape[1] * 1/2, 
                                                      image.shape[1] * 1/2],
         [image.shape[0] * 2/3, image.shape[0] * 2/3, image.shape[1] * 0/3, 
                                                      image.shape[1] * 1/3],
         [image.shape[0] * 1/3, image.shape[0] * 1/3, image.shape[1] * 0/3, 
                                                      image.shape[1] * 1/3],
         [image.shape[0] * 1/3, image.shape[0] * 2/3, image.shape[1] * 1/2, 
                                                      image.shape[1] * 1/2]] 
    i = 0
    while(i < 7):
        if(Iswhite(image, int(tubo_roi[i][0]), int(tubo_roi[i][1]), 
            int(tubo_roi[i][2]),int(tubo_roi[i][3]))):
            tube = tube + pow(2,i)
            
        cv2.line(image, ( int(tubo_roi[i][3]),int(tubo_roi[i][1])), 
                (int(tubo_roi[i][2]), int(tubo_roi[i][0])),                
                (255,0,0), 1)                       
        i += 1
 
    if(tube==63):
        onenumber = 0
    elif(tube==6):
        onenumber = 1
    elif(tube==91):
        onenumber = 2
    elif(tube==79):
        onenumber = 3
    elif(tube==102 or tube==110):
        onenumber = 4
    elif(tube==109):
        onenumber = 5
    elif(tube==125 or tube==124):
        onenumber = 6
    elif(tube==7 or tube==15):
        onenumber = 7
    elif(tube==127):
        onenumber = 8
    elif(tube==103):
        onenumber = 9
    else:
        onenumber = -1 
    # print("tube : %s -**- number is : %s "%(str(tube),str(onenumber)))
    print("number : %s "%(str(onenumber)))

    return onenumber      
 
def Iswhite(image, row_start, row_end, col_start, col_end):
    white_num = 0
    j=row_start
    i=col_start
 
    while(j <= row_end):
        while(i <= col_end):
            if(image[j][i] == 255):                
                white_num+=1
            i+=1
        j+=1
        i=col_start
    #print('white num is',white_num)
    if(white_num >= 5):
        return True
    else:
        return False


def digitalrec(image):  
    image_org = cv2.imread(image)

    # hsv
    # hsv = cv.cvtColor(image_org, cv.COLOR_BGR2HSV)
    # lower_hsv = np.array([156, 43, 46]) #156
    # upper_hsv = np.array([180, 255, 255]) # 180
    # mask = cv.inRange(hsv, lowerb=lower_hsv, upperb=upper_hsv)
    # dst = cv.bitwise_and(image_org, image_org, mask=mask)

    #transe image to gray
    image_gray = cv2.cvtColor(image_org, cv2.COLOR_RGB2GRAY)    

    meanvalue = image_gray.mean()  # meanvalue + 65
    # print("meanvalue",meanvalue)               

    ret, image_bin = cv2.threshold(image_gray, 220, 255,cv2.THRESH_BINARY) #220

    gray_res = cv2.resize(image_bin,None,fx=1,fy=1,interpolation = cv2.INTER_CUBIC)   

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))   
    # 去白點
    Open_img = cv2.morphologyEx(gray_res, cv2.MORPH_OPEN, kernel,iterations=1) 
    # 處理線之間縫隙
    Closed_img = cv2.morphologyEx(Open_img, cv2.MORPH_CLOSE, kernel,iterations=6)  

    cv2.imshow("Closed_img",Closed_img) 
    # cv2.waitKey()
    # cv2.destroyAllWindows()

    cnts, hierarchy = cv2.findContours(Closed_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  
    cnts, boundingBoxes = contours.sort_contours(cnts, method = "left-to-right")
    for i in range(0,len(cnts)):  
        x, y, w, h = cv2.boundingRect(cnts[i])    
        # cv2.rectangle(Closed_img, (x,y), (x+w,y+h), (153,153,0), 2) 
        # cv2.imshow("Closed_img",Closed_img) 
        # cv2.waitKey()
        # cv2.destroyAllWindows()
        
        # Height > Width  
        if h > w and h/w > 3 :
            # print("x : ",x,"y : ",y,"w : ",w,"h : ",h) 
            Spimg = Closed_img[y+2:y+h-2,x-70:x+w+20]  
            # cv2.imwrite("Result/Result_img/Contours1.jpg",Spimg)   
            number = TubeIdentification(Spimg)
            #cv2.imwrite("Result/Result_img/Line1.jpg",Spimg) 
            if number != -1 :
                cv2.rectangle(image_org, (x-80,y), (x+w+2,y+h), (153,153,0), 2)
                cv2.putText(image_org, str(number), (x-70,y-5), cv2.FONT_HERSHEY_SIMPLEX,4, (0, 0, 255), 5, cv2.LINE_AA)

        elif h > w:
            # print("x : ",x,"y : ",y,"w : ",w,"h : ",h) 
            Spimg = Closed_img[y+2:y+h-2,x+2:x+w-2]  
            # cv2.imwrite("Result/Result_img/ContoursD"+str(i)+".jpg",Spimg) 
            number = TubeIdentification(Spimg)
            #cv2.imwrite("Result/Result_img/Line9.jpg",Spimg) 
            if number != -1 :
                cv2.rectangle(image_org, (x,y), (x+w,y+h), (153,153,0), 2)
                cv2.putText(image_org, str(number), (x,y-5), cv2.FONT_HERSHEY_SIMPLEX,4, (0, 0, 255), 5, cv2.LINE_AA)
        else :
            pass

    cv2.imshow("ctos_img",image_org)  
    # cv2.imwrite("Result/Result_img/ResultB.jpg",image_org)
    # cv2.imwrite("Result/"+str(i)+".jpg",Spimg)
    cv2.waitKey()
    cv2.destroyAllWindows()

    #return result

if __name__ == '__main__':
    import os
    for img in os.listdir("./SSOCR/images/") :
        print(img)
        digitalrec("./SSOCR/images/"+img) 

    # digitalrec("./SSOCR/images/D.png") # D.png 8.PNG
