import sys
import os
import cv2
import numpy as np
from angle import math_angle
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QFileDialog, QMainWindow

from UserForm import Ui_MainWindow
from Gauge_Pointer import Gauge
from Seven_Segment import Segment
from Perspective import Transform

class PyQtMainEntry(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.cap = cv2.VideoCapture(0)
        #self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
        #self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)
        self.separation = 10.0 
        self.interval = int(360 / self.separation)
        self.text_offset_x = 5
        self.text_offset_y = 0
        self.Min_Value = 0
        self.Max_Value = 200
        self.Min_Angle = 45
        self.Max_Angle = 103
        self.Series_Angle = 61
        self.Center_Settings = False
        self.MaxAngle_Settings = False
        self.MinAngle_Settings = False
        self.Value_Settings = False
        self.ImageRoom = False
        self.label_1.setText("Max Value : %s"%str(self.Max_Value))
        self.label_2.setText("Max Angle : %s"%str(self.Max_Angle))
        self.label_3.setText("Min Value : %s"%str(self.Min_Value))
        self.label_4.setText("Min Angle : %s"%str(self.Min_Angle))

    def Start_7Segment(self) :
        print("Start_7Segment")
        self.cap.release()
        Segment.main()
        
    def Start_Gauge(self) :
        print("Start_Gauge")
        self.cap.release()
        if self.ImageRoom :
            Gauge.Gauge_Reader(int(self.Min_Value), int(self.Max_Value), self.Min_Angle, self.Max_Angle, int(self.CenterX/2), int(self.CenterY/2))
        else :
            Gauge.Gauge_Reader(int(self.Min_Value), int(self.Max_Value), self.Min_Angle, self.Max_Angle, self.CenterX, self.CenterY)
 
    def Out_Setting(self) :
        #print("Out_Setting")
        with open('./Parameter.txt', 'w') as file:
            if self.ImageRoom :
                file.write(str(self.Min_Value) + "," + str(self.Max_Value) + "," + str(self.Min_Angle) + "," + str(self.Max_Angle) + "," + str(int(self.CenterX/2)) + "," + str(int(self.CenterY/2)))
            else :
                file.write(str(self.Min_Value) + "," + str(self.Max_Value) + "," + str(self.Min_Angle) + "," + str(self.Max_Angle) + "," + str(int(self.CenterX)) + "," + str(int(self.CenterY)))
        file.close()


    def Value_Setting(self):
        self.Value_Settings = True
        #print("Value_Settings")

    def Check_Value(self):
        if self.Value_Settings :
            self.Value_Settings = False
            self.Max_Value = self.lineEdit.text()
            self.Min_Value = self.lineEdit_2.text()
            self.label_1.setText("Max Value : %s"%str(self.Max_Value))
            self.label_3.setText("Min Value : %s"%str(self.Min_Value))
            self.lineEdit.setText('Max_Value')
            self.lineEdit_2.setText('Min_Value')
            #print("Check_Value")

    def Add_Line_Length(self):
        # Loading New Iamge
        self.Line_set += 0.1

        if self.MaxAngle_Settings :
            Image = cv2.resize(self.frame,(self.Image_Width,self.Image_Heigh), interpolation=cv2.INTER_AREA)

            SAng = self.Max_Angle/10 + 9
            new_x = self.CenterX - self.text_offset_x + self.Line_set * 300 * np.cos((self.separation) * (SAng+9) * 3.14 / 180)
            new_y = self.CenterY + self.text_offset_y + self.Line_set * 300 * np.sin((self.separation) * (SAng+9) * 3.14 / 180)
            # cv2.putText(Image, '%s' %(int(SAng*self.separation)-90), (int(new_x), int(new_y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),1,cv2.LINE_AA)
            cv2.line(Image, (self.CenterX, self.CenterY), (int(new_x), int(new_y)),(0, 255, 0), 2)

            Image = cv2.cvtColor(Image, cv2.COLOR_BGR2RGB)
            self.QImage = QImage(Image.data, Image.shape[1],Image.shape[0], Image.shape[1]*3, QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(self.QImage))

        elif self.MinAngle_Settings :
            Image = cv2.resize(self.frame,(self.Image_Width,self.Image_Heigh), interpolation=cv2.INTER_AREA)
        
            SAng = self.Min_Angle/10 + 9
            new_x = self.CenterX - self.text_offset_x + self.Line_set * 300 * np.cos((self.separation) * (SAng+9) * 3.14 / 180)
            new_y = self.CenterY + self.text_offset_y + self.Line_set * 300 * np.sin((self.separation) * (SAng+9) * 3.14 / 180)
            # cv2.putText(Image, '%s' %(int(SAng*self.separation)-90), (int(new_x), int(new_y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),1,cv2.LINE_AA)
            cv2.line(Image, (self.CenterX, self.CenterY), (int(new_x), int(new_y)),(0, 255, 0), 2)

            Image = cv2.cvtColor(Image, cv2.COLOR_BGR2RGB)
            self.QImage = QImage(Image.data, Image.shape[1],Image.shape[0], Image.shape[1]*3, QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(self.QImage))

        else :
            pass
        #print("Add Angel Line Length")

    def Reduce_Line_Length(self):
        # Loading New Iamge
        self.Line_set -= 0.1

        if self.MaxAngle_Settings :
            Image = cv2.resize(self.frame,(self.Image_Width,self.Image_Heigh), interpolation=cv2.INTER_AREA)

            SAng = self.Max_Angle/10 + 9
            new_x = self.CenterX - self.text_offset_x + self.Line_set * 300 * np.cos((self.separation) * (SAng+9) * 3.14 / 180)
            new_y = self.CenterY + self.text_offset_y + self.Line_set * 300 * np.sin((self.separation) * (SAng+9) * 3.14 / 180)
            # cv2.putText(Image, '%s' %(int(SAng*self.separation)-90), (int(new_x), int(new_y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),1,cv2.LINE_AA)
            cv2.line(Image, (self.CenterX, self.CenterY), (int(new_x), int(new_y)),(0, 255, 0), 2)

            Image = cv2.cvtColor(Image, cv2.COLOR_BGR2RGB)
            self.QImage = QImage(Image.data, Image.shape[1],Image.shape[0], Image.shape[1]*3, QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(self.QImage))

        elif self.MinAngle_Settings :
            Image = cv2.resize(self.frame,(self.Image_Width,self.Image_Heigh), interpolation=cv2.INTER_AREA)
        
            SAng = self.Min_Angle/10 + 9
            new_x = self.CenterX - self.text_offset_x + self.Line_set * 300 * np.cos((self.separation) * (SAng+9) * 3.14 / 180)
            new_y = self.CenterY + self.text_offset_y + self.Line_set * 300 * np.sin((self.separation) * (SAng+9) * 3.14 / 180)
            # cv2.putText(Image, '%s' %(int(SAng*self.separation)-90), (int(new_x), int(new_y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),1,cv2.LINE_AA)
            cv2.line(Image, (self.CenterX, self.CenterY), (int(new_x), int(new_y)),(0, 255, 0), 2)

            Image = cv2.cvtColor(Image, cv2.COLOR_BGR2RGB)
            self.QImage = QImage(Image.data, Image.shape[1],Image.shape[0], Image.shape[1]*3, QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(self.QImage))

        else :
            pass
        #print("Reduce Angle Line Length")

    def Refresh_Image(self):
        #print("Refresh_Image")
        if self.cap.isOpened() :
            ret, self.frame = self.cap.read()
            self.frame = Transform.Trans(self.frame)
        else :
            self.cap = cv2.VideoCapture(0)
            #self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
            #self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)
            ret, self.frame = self.cap.read()
            self.frame = Transform.Trans(self.frame)

            # 視角轉換

        if 960 / self.frame.shape[1] > 2 :
            self.ImageRoom = True
            self.Image_Width = self.frame.shape[1] * 2
            self.Image_Heigh = self.frame.shape[0] * 2
            self.CenterX = int(self.frame.shape[1])
            self.CenterY = int(self.frame.shape[0] * 1.32)
            self.Line_set = 1.4
        elif self.frame.shape[1] >= 960 :
            self.ImageRoom = True
            self.Image_Width = 960
            self.Image_Heigh = 540
            self.CenterX = 480
            self.CenterY = 405
            self.Line_set = 1.3
        else :
            self.ImageRoom = False
            self.Image_Width = self.frame.shape[1]
            self.Image_Heigh = self.frame.shape[0]
            self.CenterX = int(self.frame.shape[1]/2)
            self.CenterY = int(self.frame.shape[0]*0.75)
            self.Line_set = 0.7

        Image = cv2.resize(self.frame, (self.Image_Width,self.Image_Heigh), interpolation=cv2.INTER_AREA)
        Image = cv2.cvtColor(Image, cv2.COLOR_BGR2RGB)
        self.QImage = QImage(Image.data, Image.shape[1],Image.shape[0], Image.shape[1]*3, QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(self.QImage))
        
        # self.update()

    def Center_Setting(self):
        # Loading New Iamge
        #print("Center_Settings")
        Image = cv2.resize(self.frame,(self.Image_Width,self.Image_Heigh), interpolation=cv2.INTER_AREA)

        cv2.line(Image, (self.CenterX,0), (self.CenterX,self.CenterY),(0, 255, 0), 2)
        cv2.line(Image, (self.CenterX,self.CenterY), (self.CenterX,self.Image_Heigh),(0, 255, 0), 2)
        cv2.line(Image, (0,self.CenterY), (self.CenterX,self.CenterY),(255, 0, 0), 2)
        cv2.line(Image, (self.CenterX,self.CenterY), (self.Image_Width,self.CenterY),(255, 0, 0), 2)
        Image = cv2.cvtColor(Image, cv2.COLOR_BGR2RGB)
        self.QImage = QImage(Image.data, Image.shape[1],Image.shape[0], Image.shape[1]*3, QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(self.QImage))

        self.Center_Settings = True
        self.MaxAngle_Settings = False
        self.MinAngle_Settings = False
        self.Value_Settings = False

    def MaxAngle_Setting(self):
        # Loading New Iamge
        #print("MaxAngle_Settings")
        Image = cv2.resize(self.frame,(self.Image_Width,self.Image_Heigh), interpolation=cv2.INTER_AREA)

        SAng = self.Max_Angle/10 + 9
        new_x = self.CenterX - self.text_offset_x + self.Line_set * 300 * np.cos((self.separation) * (SAng+9) * 3.14 / 180)
        new_y = self.CenterY + self.text_offset_y + self.Line_set * 300 * np.sin((self.separation) * (SAng+9) * 3.14 / 180)
        # cv2.putText(Image, '%s' %(int(SAng*self.separation)-90), (int(new_x), int(new_y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),1,cv2.LINE_AA)
        cv2.line(Image, (self.CenterX, self.CenterY), (int(new_x), int(new_y)),(0, 255, 0), 2)

        Image = cv2.cvtColor(Image, cv2.COLOR_BGR2RGB)
        self.QImage = QImage(Image.data, Image.shape[1],Image.shape[0], Image.shape[1]*3, QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(self.QImage))

        self.Center_Settings = False
        self.MaxAngle_Settings = True
        self.MinAngle_Settings = False
        self.Value_Settings = False

    def MinAngle_Setting(self):
        # Loading New Iamge
        #print("MinAngle_Settings")
        Image = cv2.resize(self.frame,(self.Image_Width,self.Image_Heigh), interpolation=cv2.INTER_AREA)
        
        SAng = self.Min_Angle/10 + 9
        new_x = self.CenterX - self.text_offset_x + self.Line_set * 300 * np.cos((self.separation) * (SAng+9) * 3.14 / 180)
        new_y = self.CenterY + self.text_offset_y + self.Line_set * 300 * np.sin((self.separation) * (SAng+9) * 3.14 / 180)
        # cv2.putText(Image, '%s' %(int(SAng*self.separation)-90), (int(new_x), int(new_y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),1,cv2.LINE_AA)
        cv2.line(Image, (self.CenterX, self.CenterY), (int(new_x), int(new_y)),(0, 255, 0), 2)

        Image = cv2.cvtColor(Image, cv2.COLOR_BGR2RGB)
        self.QImage = QImage(Image.data, Image.shape[1],Image.shape[0], Image.shape[1]*3, QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(self.QImage))
        
        self.Center_Settings = False
        self.MaxAngle_Settings = False
        self.MinAngle_Settings = True
        self.Value_Settings = False

    def Move_Up(self):
        if self.Center_Settings :
            self.CenterY -= 1
            Image = cv2.resize(self.frame,(self.Image_Width,self.Image_Heigh), interpolation=cv2.INTER_AREA)

            cv2.line(Image, (self.CenterX,0), (self.CenterX,self.CenterY),(0, 255, 0), 2)
            cv2.line(Image, (self.CenterX,self.CenterY), (self.CenterX,self.Image_Heigh),(0, 255, 0), 2)
            cv2.line(Image, (0,self.CenterY), (self.CenterX,self.CenterY),(255, 0, 0), 2)
            cv2.line(Image, (self.CenterX,self.CenterY), (self.Image_Width,self.CenterY),(255, 0, 0), 2)
            Image = cv2.cvtColor(Image, cv2.COLOR_BGR2RGB)
            self.QImage = QImage(Image.data, Image.shape[1],Image.shape[0], Image.shape[1]*3, QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(self.QImage))
            #print("Move_Up ---- Now px : ", self.CenterX)

    def Move_Down(self):
        if self.Center_Settings :
            self.CenterY += 1
            Image = cv2.resize(self.frame,(self.Image_Width,self.Image_Heigh), interpolation=cv2.INTER_AREA)
            cv2.line(Image, (self.CenterX,0), (self.CenterX,self.CenterY),(0, 255, 0), 2)
            cv2.line(Image, (self.CenterX,self.CenterY), (self.CenterX,self.Image_Heigh),(0, 255, 0), 2)
            cv2.line(Image, (0,self.CenterY), (self.CenterX,self.CenterY),(255, 0, 0), 2)
            cv2.line(Image, (self.CenterX,self.CenterY), (self.Image_Width,self.CenterY),(255, 0, 0), 2)
            Image = cv2.cvtColor(Image, cv2.COLOR_BGR2RGB)
            self.QImage = QImage(Image.data, Image.shape[1],Image.shape[0], Image.shape[1]*3, QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(self.QImage))
            #print("Move_Down ---- Now px : ", self.CenterX)    

    def Move_Left(self):
        if self.Center_Settings :
            self.CenterX -= 1
            Image = cv2.resize(self.frame,(self.Image_Width,self.Image_Heigh), interpolation=cv2.INTER_AREA)

            cv2.line(Image, (self.CenterX,0), (self.CenterX,self.CenterY),(0, 255, 0), 2)
            cv2.line(Image, (self.CenterX,self.CenterY), (self.CenterX,self.Image_Heigh),(0, 255, 0), 2)
            cv2.line(Image, (0,self.CenterY), (self.CenterX,self.CenterY),(255, 0, 0), 2)
            cv2.line(Image, (self.CenterX,self.CenterY), (self.Image_Width,self.CenterY),(255, 0, 0), 2)
            Image = cv2.cvtColor(Image, cv2.COLOR_BGR2RGB)
            self.QImage = QImage(Image.data, Image.shape[1],Image.shape[0], Image.shape[1]*3, QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(self.QImage))
            #print("Move_Left ---- Now px : ", self.CenterX)

    def Move_Right(self):
        if self.Center_Settings :
            self.CenterX += 1
            Image = cv2.resize(self.frame,(self.Image_Width,self.Image_Heigh), interpolation=cv2.INTER_AREA)

            cv2.line(Image, (self.CenterX,0), (self.CenterX,self.CenterY),(0, 255, 0), 2)
            cv2.line(Image, (self.CenterX,self.CenterY), (self.CenterX,self.Image_Heigh),(0, 255, 0), 2)
            cv2.line(Image, (0,self.CenterY), (self.CenterX,self.CenterY),(255, 0, 0), 2)
            cv2.line(Image, (self.CenterX,self.CenterY), (self.Image_Width,self.CenterY),(255, 0, 0), 2)
            Image = cv2.cvtColor(Image, cv2.COLOR_BGR2RGB)
            self.QImage = QImage(Image.data, Image.shape[1],Image.shape[0], Image.shape[1]*3, QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(self.QImage))
            #print("Move_Right ---- Now px : ", self.CenterX)

    def Check_Center(self):
        # Loading New Iamge
        if self.Center_Settings :
            #print("Check_Center")
            self.Center_Settings = False
            Image = cv2.resize(self.frame,(self.Image_Width,self.Image_Heigh), interpolation=cv2.INTER_AREA)

        Image = cv2.cvtColor(Image, cv2.COLOR_BGR2RGB)
        self.QImage = QImage(Image.data, Image.shape[1],Image.shape[0], Image.shape[1]*3, QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(self.QImage))
        
    def Angle_Add(self):
        if self.MaxAngle_Settings :
            self.Max_Angle += 1
            self.label_2.setText("Max Angle : %s"%str(self.Max_Angle))
            Image = cv2.resize(self.frame,(self.Image_Width,self.Image_Heigh), interpolation=cv2.INTER_AREA)

            SAng = self.Max_Angle/10 + 9
            new_x = self.CenterX - self.text_offset_x + self.Line_set * 300 * np.cos((self.separation) * (SAng+9) * 3.14 / 180)
            new_y = self.CenterY + self.text_offset_y + self.Line_set * 300 * np.sin((self.separation) * (SAng+9) * 3.14 / 180)
            # cv2.putText(Image, '%s' %(int(SAng*self.separation)-90), (int(new_x), int(new_y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),1,cv2.LINE_AA)
            cv2.line(Image, (self.CenterX, self.CenterY), (int(new_x), int(new_y)),(0, 255, 0), 2)

            Image = cv2.cvtColor(Image, cv2.COLOR_BGR2RGB)
            self.QImage = QImage(Image.data, Image.shape[1],Image.shape[0], Image.shape[1]*3, QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(self.QImage))

            #print("MaxAngle_Settings Angle_Add Now Angle : ", self.Max_Angle)
        elif self.MinAngle_Settings :
            self.Min_Angle += 1
            self.label_4.setText("Min Angle : %s"%str(self.Min_Angle))

            Image = cv2.resize(self.frame,(self.Image_Width,self.Image_Heigh), interpolation=cv2.INTER_AREA)
        
            SAng = self.Min_Angle/10 + 9
            new_x = self.CenterX - self.text_offset_x + self.Line_set * 300 * np.cos((self.separation) * (SAng+9) * 3.14 / 180)
            new_y = self.CenterY + self.text_offset_y + self.Line_set * 300 * np.sin((self.separation) * (SAng+9) * 3.14 / 180)
            # cv2.putText(Image, '%s' %(int(SAng*self.separation)-90), (int(new_x), int(new_y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),1,cv2.LINE_AA)
            cv2.line(Image, (self.CenterX, self.CenterY), (int(new_x), int(new_y)),(0, 255, 0), 2)

            Image = cv2.cvtColor(Image, cv2.COLOR_BGR2RGB)
            self.QImage = QImage(Image.data, Image.shape[1],Image.shape[0], Image.shape[1]*3, QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(self.QImage))

            #print("MinAngle_Settings  Angle_Add Now Angle : ", self.Min_Angle)
        else :
            pass

    def Angle_Reduce(self):
        if self.MaxAngle_Settings :
            self.Max_Angle -= 1
            self.label_2.setText("Max Angle : %s"%str(self.Max_Angle))

            Image = cv2.resize(self.frame,(self.Image_Width,self.Image_Heigh), interpolation=cv2.INTER_AREA)

            SAng = self.Max_Angle/10 + 9
            new_x = self.CenterX - self.text_offset_x + self.Line_set * 300 * np.cos((self.separation) * (SAng+9) * 3.14 / 180)
            new_y = self.CenterY + self.text_offset_y + self.Line_set * 300 * np.sin((self.separation) * (SAng+9) * 3.14 / 180)
            # cv2.putText(Image, '%s' %(int(SAng*self.separation)-90), (int(new_x), int(new_y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),1,cv2.LINE_AA)
            cv2.line(Image, (self.CenterX, self.CenterY), (int(new_x), int(new_y)),(0, 255, 0), 2)

            Image = cv2.cvtColor(Image, cv2.COLOR_BGR2RGB)
            self.QImage = QImage(Image.data, Image.shape[1],Image.shape[0], Image.shape[1]*3, QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(self.QImage))

            #print("MaxAngle_Settings Angle_Add Now Angle : ", self.Max_Angle)
        elif self.MinAngle_Settings :
            self.Min_Angle -= 1
            self.label_4.setText("Min Angle : %s"%str(self.Min_Angle))

            Image = cv2.resize(self.frame,(self.Image_Width,self.Image_Heigh), interpolation=cv2.INTER_AREA)
        
            SAng = self.Min_Angle/10 + 9
            new_x = self.CenterX - self.text_offset_x + self.Line_set * 300 * np.cos((self.separation) * (SAng+9) * 3.14 / 180)
            new_y = self.CenterY + self.text_offset_y + self.Line_set * 300 * np.sin((self.separation) * (SAng+9) * 3.14 / 180)
            # cv2.putText(Image, '%s' %(int(SAng*self.separation)-90), (int(new_x), int(new_y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),1,cv2.LINE_AA)
            cv2.line(Image, (self.CenterX, self.CenterY), (int(new_x), int(new_y)),(0, 255, 0), 2)

            Image = cv2.cvtColor(Image, cv2.COLOR_BGR2RGB)
            self.QImage = QImage(Image.data, Image.shape[1],Image.shape[0], Image.shape[1]*3, QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(self.QImage))

            #print("MinAngle_Settings  Angle_Add Now Angle : ", self.Min_Angle)
        else :
            pass
    def Check_Angle(self):
        # Loading New Iamge
        if self.MaxAngle_Settings :
            #print("MaxAngle_Settings Check_Angle")
            self.MaxAngle_Settings = False
        elif self.MinAngle_Settings :
            #print("MaxAngle_Settings Check_Angle")
            self.MaxAngle_Settings = False
        else :
            pass
        Image = cv2.resize(self.frame,(self.Image_Width,self.Image_Heigh), interpolation=cv2.INTER_AREA)

        Image = cv2.cvtColor(Image, cv2.COLOR_BGR2RGB)
        self.QImage = QImage(Image.data, Image.shape[1],Image.shape[0], Image.shape[1]*3, QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(self.QImage))
        
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    print(app)
    window = PyQtMainEntry()
    window.show()
    sys.exit(app.exec_())
