
import time
import cv2
import os
import numpy as np
import random
import datetime
from mss import mss
from datetime import date
import pytz
import mouse
import serial
import logging
import serial.tools.list_ports
import subprocess

import threading
import time


class MyThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

        self.check_callback = callback
        self.embaixo = np.array([140,105,60])
        self.emcima = np.array([150,200,200])
        self.arduino = None
        self.lasdx=0
        self.lasdy=0
        self.g_workmode=1
        self.comname=""
        self.iscomok=False
    def run(self):
        while self.iscomok==False:
            self.getArduinoCom()
            time.sleep(2)

        self.update_signal.emit(6)

        self.dowork()
    def getArduinoCom(self):
        ports = serial.tools.list_ports.comports()
        for port, desc, hwid in sorted(ports):
            print(f"{port}: {desc}")
            logging.info(f"{port}: {desc}")  
            if "Arduino Leonardo" in desc:
                self.comname=port
                break
        if len(self.comname)>1:

            command = ['avrdude', '-v', '-Cavrdude.conf', '-patmega32u4', '-cavr109', f'-P{self.comname}', '-b9600', '-D', '-Uflash:w:2.hex:i']

            result = subprocess.run(command, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            outstr=result.stdout+result.stderr

            if "avrdude done." in outstr:
                time.sleep(3)
                self.arduino = serial.Serial('COM3', 115200)
                self.iscomok=True
            else:
                logging.info(f"avrdude cmd: {outstr}" )  

        else:
            logging.info("NO Arduino")  
            self.update_signal.emit(9)

    def is_BN9_key_pressed(self,type):

        if type==1:
            mouse.wait(button='left', target_types=('down'))
        if type==2:
            mouse.wait(button='right', target_types=('down'))
        return True
    def dowork(self):
        self.sct = mss()
        self.screenshot = self.sct.monitors[1]
        self.scwith=self.screenshot['width']/2
        self.scheight=self.screenshot['height']/2
   
        while True:
            iswork=False
        
            if self.g_workmode==1:
                if self.is_BN9_key_pressed(1):
                    iswork=True
                    self.cvwork()
            if self.g_workmode==2:
                if self.is_BN9_key_pressed(2):
                    iswork=True
                    self.cvwork()
            time.sleep(0.01)

    def calculate_distance( self,head_center,diameter):

        new_head_center= self.debug_postion(head_center,diameter)

        distance = (400 // 2 - new_head_center[0], 400// 2 - new_head_center[1])

        distance = tuple(-(i//1) for i in distance) # reverse sign
        ndis=self.debug_dis(distance)
        return ndis

    #微调坐标到头部处理
    def debug_postion(self, pos,diameter):
        dy=pos[1]+7
        dx=pos[0]
        new_pos = (dx, dy)
        return new_pos
    
    def cvwork(self):

        self.screenshot['left'] = int(self.scwith - (400 / 2))
        self.screenshot['top'] = int(self.scheight - (400 / 2))
        self.screenshot['width'] = 400
        self.screenshot['height'] = 400
        img = np.array(self.sct.grab(self.screenshot))

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.embaixo,self.emcima)
        kernel = np.ones((3,3), np.uint8)
        dilated = cv2.dilate(mask,kernel,iterations= 5)
        thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)# #CHAIN_APPROX_NONE

        if len(contours) != 0:

            c = max(contours, key=cv2.contourArea)

            rect = cv2.minAreaRect(c)

            width, height = rect[1]

            diameter = max(width, height)
            topmost = tuple(c[c[:,:,1].argmin()][0])

            rvmouse = cv2.moments(thresh)
            pixel = (int(rvmouse["m10"] / rvmouse["m00"]), int(rvmouse["m01"] / rvmouse["m00"]))
            aimzao=(pixel[0],topmost[1])
            distance=self.calculate_distance(aimzao,diameter)
            if abs(distance[0]-self.lasdx)<3 and abs(distance[1]-self.lasdy)<3:
                time.sleep(0.01)
                return
            self.lasdx=distance[0]
            self.lasdy=distance[1]
            
            serial_message = f"{distance[0]},{distance[1]}\n"

            self.arduino.write(str.encode(serial_message))
            time.sleep(0.01)







thread1 = MyThread("Thread 1")
thread1.start()