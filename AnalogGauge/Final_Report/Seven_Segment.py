import cv2
import numpy as np
from imutils import contours
import cv2 as cv
import time
#from moviepy.editor import VideoFileClip, concatenate_videoclips

class Segment() :
    def smain() :
        # img = cv2.imread("b.PNG")
        # cv2.imshow('img',img)
        # cv2.waitKey()
        # cv2.destroyAllWindows()
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)
        while cap.isOpened() :
            ret, image_org = cap.read()
            cv2.imshow('frame',image_org)

            if cv2.waitKey(1) & 0xFF == ord('q'):  
                break
        cap.release()
        cv2.destroyAllWindows()

    def main() :
        cap = cv2.VideoCapture(0)#"rtsp://192.168.0.168"
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)
        count = 0
        Sort_number, reg_number = 0, 0
        while cap.isOpened() :
            ret, image_org = cap.read()
            if ret :
                # if count % 30 == 0:
                Closed_img, image_org, Sort_number = Segment.digitalrec(image_org)
                if Sort_number != reg_number and Sort_number != 0:
                    print("Sort_number : ", Sort_number)
                    reg_number = Sort_number

                cv2.imshow('Closed_img',Closed_img)
                cv2.imshow('frame',image_org)
            else : 
                break

            count += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):  
                break

        cap.release()
        cv2.destroyAllWindows()

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
            [image.shape[0] * 0/3, image.shape[0] * 1/3, image.shape[1] * 1/2, image.shape[1] * 1/2],
            [image.shape[0] * 1/3, image.shape[0] * 1/3, image.shape[1] * 2/3, image.shape[1] - 1  ],
            [image.shape[0] * 2/3, image.shape[0] * 2/3, image.shape[1] * 2/3, image.shape[1] - 1  ],
            [image.shape[0] * 2/3, image.shape[0] -1   , image.shape[1] * 1/2, image.shape[1] * 1/2],
            [image.shape[0] * 2/3, image.shape[0] * 2/3, image.shape[1] * 0/3, image.shape[1] * 1/3],
            [image.shape[0] * 1/3, image.shape[0] * 1/3, image.shape[1] * 0/3, image.shape[1] * 1/3],
            [image.shape[0] * 1/3, image.shape[0] * 2/3, image.shape[1] * 1/2, image.shape[1] * 1/2]] 
        i = 0
        while(i < 7):
            if(Segment.Iswhite(image, int(tubo_roi[i][0]), int(tubo_roi[i][1]), 
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
        # print("number : %s "%(str(onenumber)))

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


    def digitalrec(image_org):  
        number_List = []
        # image_org = cv2.imread(image)
        # image_org = image.copy()

        # hsv
        # hsv = cv.cvtColor(image_org, cv.COLOR_BGR2HSV)
        # lower_hsv = np.array([156, 43, 46]) #156
        # upper_hsv = np.array([180, 255, 255]) # 180
        # mask = cv.inRange(hsv, lowerb=lower_hsv, upperb=upper_hsv)
        # dst = cv.bitwise_and(image_org, image_org, mask=mask)

        #transefer image to gray
        image_gray = cv2.cvtColor(image_org, cv2.COLOR_RGB2GRAY)    

        meanvalue = image_gray.mean()  # meanvalue + 65
        # print("meanvalue",meanvalue)               

        ret, image_bin = cv2.threshold(image_gray, 230, 255,cv2.THRESH_BINARY) #220
        # cv2.imshow("image_bin",image_bin) 

        gray_res = cv2.resize(image_bin,None,fx=1,fy=1,interpolation = cv2.INTER_CUBIC)   

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))  
        # 去白點
        Open_img = cv2.morphologyEx(gray_res, cv2.MORPH_OPEN, kernel,iterations=1) 
        # 處理線之間縫隙
        Closed_img = cv2.morphologyEx(Open_img, cv2.MORPH_CLOSE, kernel,iterations=5) 

        #kernel = np.ones((3,3), np.uint8)
        #Closed_img = cv2.dilate(Closed_img, kernel, iterations = 1) 
        
        # cv2.imshow("gray_res",gray_res)
        # cv2.imshow("Open_img",Open_img)
        # cv2.imshow("Closed_img",Closed_img) 
        # cv2.waitKey()
        # cv2.destroyAllWindows()
        
        try :
            try : 
                excep, cnts, hierarchy = cv2.findContours(Closed_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  
                cnts, boundingBoxes = contours.sort_contours(cnts, method = "left-to-right")
            except Exception as e:
                print(e)

            for i in range(0,len(cnts)):  
                x, y, w, h = cv2.boundingRect(cnts[i])    
                cv2.rectangle(Closed_img, (x,y), (x+w,y+h), (255,0,0), 2)
                # print("x : ",x,"y : ",y,"w : ",w,"h : ",h) 
                # Height > Width  
                if h > w and h/w > 2.5 and h > 45 :
                    # print("if x : ",x,"y : ",y,"w : ",w,"h : ",h)
                    cv2.rectangle(Closed_img, (x-20,y), (x+w+2,y+h), (255,0,0), 2)
                    Spimg = Closed_img[y+2:y+h-2,x-20:x+w]  
                    # cv2.imwrite("Result/Result_img/Contours1.jpg",Spimg)   
                    number = Segment.TubeIdentification(Spimg)
                    #cv2.imwrite("Result/Result_img/Line1.jpg",Spimg) 
                    if number != -1 :
                        number_List.append(number)
                        # cv2.rectangle(image_org, (x-80,y), (x+w+2,y+h), (153,153,0), 2)
                        cv2.putText(image_org, str(number), (x-20,y-5), cv2.FONT_HERSHEY_SIMPLEX,2, (0, 0, 255), 3, cv2.LINE_AA)

                elif h > w and h > 45:
                    cv2.rectangle(Closed_img, (x,y), (x+w,y+h), (255,0,0), 2)
                    # print("elif x : ",x,"y : ",y,"w : ",w,"h : ",h)
                    Spimg = Closed_img[y+2:y+h-2,x+2:x+w-2]  
                    # cv2.imwrite("Result/Result_img/ContoursD"+str(i)+".jpg",Spimg) 
                    number = Segment.TubeIdentification(Spimg)
                    #cv2.imwrite("Result/Result_img/Line9.jpg",Spimg) 
                    if number != -1 :
                        number_List.append(number)
                        # cv2.rectangle(image_org, (x,y), (x+w,y+h), (153,153,0), 2)
                        cv2.putText(image_org, str(number), (x,y-5), cv2.FONT_HERSHEY_SIMPLEX,2, (0, 0, 255), 3, cv2.LINE_AA) # 4,5
                else :
                    pass

            # cv2.imshow("ctoimg",Closed_img)
            # cv2.imshow("ctos_img",image_org)  
            # # cv2.imwrite("./image_org1.jpg",image_org)
            # # # cv2.imwrite("./Spimg.jpg",Spimg)
            # cv2.waitKey()
            # cv2.destroyAllWindows()
            if len(number_List) == 3 :
                return Closed_img, image_org, int(str(number_List[0])+str(number_List[1])+str(number_List[2]))
            else :
                return Closed_img, image_org, 0
        except Exception as e :
            print(e)
            return Closed_img, image_org, number_List


if __name__ == '__main__':
    Segment.main()


