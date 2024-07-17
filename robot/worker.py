from PyQt5.QtCore import QThread, pyqtSignal
import time
import cv2
import os
import numpy as np
import random
import globals  # 导入包含全局变量的模块
from mss import mss
import mouse
from collections import namedtuple
ButtonEvent = namedtuple('ButtonEvent', ['event_type', 'button', 'time'])
# 创建后台任务类
class Worker(QThread):
    check_status = pyqtSignal()
    update_signal = pyqtSignal(int)

    def __init__(self, callback, parent=None):
        super().__init__(parent)
        self.check_callback = callback
        #self.embaixo = np.array([140,111,60])
        #self.emcima = np.array([150,184,194])
        #self.embaixo = np.array([149,102,222])
        #self.emcima = np.array([156,204,255])
        self.embaixo = np.array([143,107,190])
        self.emcima = np.array([160,200,255])
        globals.garduino = None
        self.lasdx=0
        self.lasdy=0
        self.runtype=0
        self.downrun=False
    def run(self):
        '''
        try:
            sensitivity = mou.get_mouse_sensitivity()
            if sensitivity>0.2 and sensitivity<10.0:
                sensitivity=sensitivity-0.1
                globals.g_mouspeed=sensitivity
                self.update_signal.emit(7)
                print('globals.g_mousesp:',globals.g_mouspeed)
        except :
            pass
        '''
        # 定义一个全局变量，它将保留鼠标左键的状态
        while True:
            if globals.g_iswork==False:
                time.sleep(1)
                continue
            else:
                if globals.g_iscomok==True:
                    self.dowork()
                else:
                    #self.update_signal.emit(9)
                    time.sleep(1)
                    continue
    def sleep_milliseconds(self,milliseconds):
        start_time = time.perf_counter()
        while (time.perf_counter() - start_time) < (milliseconds / 1000):
            pass 
    def delfile(self,filename):
        if os.path.exists(filename):
            # Remove the file
            os.remove(filename)
            print(f"File {filename} has been removed.")
        else:
            print("File does not exist.")

    def is_BN9_key_pressed_callback(self,event):
        if hasattr(event, 'button')==False:
            return
        if self.runtype==5:
            if event.button == globals.RIGHT and event.event_type == globals.UP  :
                self.downrun=False
                mouse.unhook(self.is_BN9_key_pressed_callback)
        elif self.runtype==6:

            if event.button == globals.X and event.event_type == globals.UP  :
                self.downrun=False
                mouse.unhook(self.is_BN9_key_pressed_callback)
        elif self.runtype==7:
            if event.button == globals.X2 and event.event_type == globals.UP  :
                self.downrun=False
                mouse.unhook(self.is_BN9_key_pressed_callback)
    def is_BN9_key_pressed(self,type):
        #阻塞的
        from threading import Lock
        globals.glock= Lock()
        self.runtype=type
        if type==1:
            mouse.waited(globals.glock,button=globals.LEFT, target_types=(globals.DOWN,globals.DOUBLE))
        elif type==2:
            mouse.waited(globals.glock,button=globals.RIGHT, target_types=(globals.DOWN,globals.DOUBLE))
        elif type==3:
            mouse.waited(globals.glock,button=globals.X, target_types=(globals.DOWN,globals.DOUBLE))
        elif type==4:
            mouse.waited(globals.glock,button=globals.X2, target_types=(globals.DOWN,globals.DOUBLE))
        elif type==5:
            mouse.waited(globals.glock,button=globals.RIGHT, target_types=(globals.DOWN))
            if globals.g_workmode!=2:
                return
            self.downrun=True
            mouse.hook(self.is_BN9_key_pressed_callback)
        elif type==6:
            mouse.waited(globals.glock,button=globals.X, target_types=(globals.DOWN))
            if globals.g_workmode!=3:
                return
            self.downrun=True
            mouse.hook(self.is_BN9_key_pressed_callback)
        elif type==7:
            mouse.waited(globals.glock,button=globals.X2, target_types=(globals.DOWN))
            if globals.g_workmode!=4:
                return
            self.downrun=True
            mouse.hook(self.is_BN9_key_pressed_callback)
        elif type==8:
            mouse.waited(globals.glock,button=globals.LEFT, target_types=(globals.DOWN))
            if globals.g_workmode!=1:
                return
            self.downrun=True
            mouse.hook(self.is_BN9_key_pressed_callback)
        return True
    def dowork(self):
        self.sct = mss()
        self.screenshot = self.sct.monitors[1]
        self.scwith=self.screenshot['width']/2
        self.scheight=self.screenshot['height']/2
        while True:
           # print('model::',globals.g_workmode)
            if globals.g_iswork==False:
                break
            iswork=False
            if globals.g_workmode==1:#点击左键
                if self.is_BN9_key_pressed(1):
                    iswork=True
                    self.cvworkapiwhile()
            elif globals.g_isancheck==False and globals.g_workmode==2:#点击右键
                if self.is_BN9_key_pressed(2):
                    iswork=True
                    self.cvworkapiwhile()
            elif globals.g_isancheck==False and globals.g_workmode==3:#
                if self.is_BN9_key_pressed(3):
                    iswork=True
                    self.cvworkapiwhile()
            elif globals.g_isancheck==False and globals.g_workmode==4:#
                if self.is_BN9_key_pressed(4):
                    iswork=True
                    self.cvworkapiwhile()
            elif globals.g_isancheck==True and globals.g_workmode==1:#
                if self.is_BN9_key_pressed(8):
                    iswork=True
                    self.whilecvwork()
            elif globals.g_isancheck==True and globals.g_workmode==2:#
                if self.is_BN9_key_pressed(5):
                    iswork=True
                    self.whilecvwork()
            elif globals.g_isancheck==True and globals.g_workmode==3:#按上侧键

                if self.is_BN9_key_pressed(6):
                    iswork=True
                    self.whilecvwork()
            elif globals.g_isancheck==True and globals.g_workmode==4:#按下下侧按键
                if self.is_BN9_key_pressed(7):
                    iswork=True
                    self.whilecvwork()
            elif globals.g_workmode==6:#
                self.runctrlmode()
                iswork=True
            elif globals.g_workmode==5:#
                if globals.gcz==True:
                    iswork=True
                    self.cvworkapi()
            if iswork==False:
               time.sleep(1) 
            else:
                self.sleep_milliseconds(3)
    def runctrlmode(self):
        while globals.g_workmode==6:#

            if globals.g_isancheck==True and globals.g_ctrlisdown==True:

                if globals.g_workcolormode==3: 
                    self.cvwork()
                elif globals.g_workcolormode==4: 
                    self.cvworkjHmodeEd()
            elif globals.g_ctrliswork==False and globals.g_ctrlisdown==True:#

                globals.g_ctrliswork=True
                self.cvworkRotApi()
            time.sleep(globals.g_tsleep) 

    def calculate_distance( self,head_center):

        distance = (globals.g_fox // 2 - head_center[0], globals.g_foy// 2 - head_center[1])
        # 5 is a step. This value must be the same in the Mouse.move function on the arduino.
        # for example: if the distance on the x-axis is 100, then we take a step of 5 units 20 times
        distance = tuple(-(i//1) for i in distance) # reverse sign
        ndis=self.debug_dis(distance)
        return ndis
    def calculate_distanceEx( self,head_center):
        #print('head_center',head_center)

        #print('new_head_center',new_head_center)
        distance = (globals.g_fox // 2 - head_center[0], globals.g_foy// 2 - head_center[1])
        # 5 is a step. This value must be the same in the Mouse.move function on the arduino.
        # for example: if the distance on the x-axis is 100, then we take a step of 5 units 20 times
        distance = tuple(-(i//1) for i in distance) # reverse sign
        ndis=self.debug_dis(distance)
        
        return ndis  
    def calculate_distanceExD( self,head_center):
        #print('head_center',head_center)

        #print('new_head_center',new_head_center)
        if  globals.gistotop==False:
            distance = (globals.g_fox // 2 - head_center[0], globals.g_foy// 2 - head_center[1])
        else:
            distance = (globals.g_topfox // 2 - head_center[0], globals.g_foy// 2 - head_center[1])
        # 5 is a step. This value must be the same in the Mouse.move function on the arduino.
        # for example: if the distance on the x-axis is 100, then we take a step of 5 units 20 times
        distance = tuple(-(i//1) for i in distance) # reverse sign
        ndis=self.debug_dis(distance)
        
        return ndis  
    #微调距离
    def debug_dis(self,distance):
        dx=distance[0]
        dy=distance[1]
        nx=int(dx*0.33*globals.g_mouspeed)
        ny=int(dy*0.33*globals.g_mouspeed)

        new_dis = (nx, ny)
        return new_dis
    def istomoseyidong(self,px,py,distance):
        if globals.g_button_yaqing==True:
            globals.g_button_yaqing=False
            return True,1
        total_seconds = time.time()
        time_diff = (total_seconds - globals.gtotal_seconds) * 1000  
        if time_diff>300:#超过了2秒，直接返回
            globals.gtotal_seconds=total_seconds
            if abs(distance[0])>15 or abs(distance[1])>15:
                return True,0
            else:
                return True,1
        if abs(distance[0])>20 or abs(distance[1])>20:
            globals.gtotal_seconds=total_seconds
            return True,0
        if abs(distance[0])>12 or abs(distance[1])>12:
            globals.gtotal_seconds=total_seconds
            return True,1
        if abs(distance[0])>4 or abs(distance[1])>4:
            globals.gtotal_seconds=total_seconds
            return True,1

        return False,0
             
    def istomoseyidongEx(self,x1,x2,y1,y2,px,py,distance):
        total_seconds = time.time()
        time_diff = (total_seconds - globals.gtotal_seconds) * 1000  
        if time_diff>300:#超过了2秒，直接返回
            globals.gtotal_seconds=total_seconds
            if abs(distance[0])>15 or abs(distance[1])>15:
                return True,0
            else:
                return True,1
        if abs(distance[0])>20 or abs(distance[1])>20:
            globals.gtotal_seconds=total_seconds
            return True,0
        if abs(distance[0])>5 or abs(distance[1])>5:
            globals.gtotal_seconds=total_seconds
            return True,1
        if abs(distance[0])>3 or abs(distance[1])>3:
            if (px <= x1 ) or (px >= x2 ) :
                globals.gtotal_seconds=total_seconds
                return True,1
        if (px <= x1 ) or (px >= x2 ) or (py<y1):
            globals.gtotal_seconds=total_seconds
            return True,0
        return False,0

    def scale_valueEx(self, max_value=150):
        # 计算分数
        scaled_value = 0.5 + 0.5 * globals.g_headwd
        return scaled_value

    #微调坐标到头部处理
    def debug_postionA(self, pos,diameter):
        ly=int(diameter*globals.g_headwd)#0.07
        dy=pos[1]+ly
        dx=pos[0]
        new_pos = (dx, dy)
        return new_pos
    def are_close(self,stat1, stat2, centroids1, centroids2, centroid_distance_threshold=12.0, overlap_threshold_x=3, overlap_threshold_y=20.0):
        # Calculate overlap on the x and y axis
        x_overlap = min(stat1[cv2.CC_STAT_LEFT] + stat1[cv2.CC_STAT_WIDTH], stat2[cv2.CC_STAT_LEFT] + stat2[cv2.CC_STAT_WIDTH]) - max(stat1[cv2.CC_STAT_LEFT], stat2[cv2.CC_STAT_LEFT])
        y_overlap = min(stat1[cv2.CC_STAT_TOP] + stat1[cv2.CC_STAT_HEIGHT], stat2[cv2.CC_STAT_TOP] + stat2[cv2.CC_STAT_HEIGHT]) - max(stat1[cv2.CC_STAT_TOP], stat2[cv2.CC_STAT_TOP])
        centroid_distance = np.sqrt((centroids1[0] - centroids2[0])**2 + (centroids1[1] - centroids2[1])**2)
        isok=False
        if x_overlap>=0:
            if abs(y_overlap)<overlap_threshold_y:
                isok=True
        elif  abs(x_overlap) < overlap_threshold_x :
            if abs(y_overlap)<(overlap_threshold_y-15):
                isok=True
        elif centroid_distance<centroid_distance_threshold:
            isok=True
        return isok
    def are_closeEd(self,stat1, stat2, centroids1, centroids2, centroid_distance_threshold=3, overlap_threshold_x=0, overlap_threshold_y=10):
                # Calculate overlap on the x and y axis
        x_overlap = min(stat1[cv2.CC_STAT_LEFT] + stat1[cv2.CC_STAT_WIDTH], stat2[cv2.CC_STAT_LEFT] + stat2[cv2.CC_STAT_WIDTH]) - max(stat1[cv2.CC_STAT_LEFT], stat2[cv2.CC_STAT_LEFT])
        y_overlap = min(stat1[cv2.CC_STAT_TOP] + stat1[cv2.CC_STAT_HEIGHT], stat2[cv2.CC_STAT_TOP] + stat2[cv2.CC_STAT_HEIGHT]) - max(stat1[cv2.CC_STAT_TOP], stat2[cv2.CC_STAT_TOP])
        centroid_distance = np.sqrt((centroids1[0] - centroids2[0])**2 + (centroids1[1] - centroids2[1])**2)
        isok=False
        if x_overlap>=0:
            if abs(y_overlap)<overlap_threshold_y:
                isok=True
        elif  abs(x_overlap) < overlap_threshold_x :
            if abs(y_overlap)<(overlap_threshold_y-15):
                isok=True
        elif centroid_distance<centroid_distance_threshold:
            isok=True
        return isok
    def whilecvwork(self):
        while self.downrun==True:
            if globals.g_workcolormode==1:
                self.cvworkjHmodeEdMustTop()
            elif globals.g_workcolormode==2: 
                 self.cvworkjHmodeEdMust()
            elif globals.g_workcolormode==3: 
                 self.cvwork()
            elif globals.g_workcolormode==4: 
                 self.cvworkjHmodeEd()
            time.sleep(globals.g_tsleep) 

    def cvworkapi(self):
        #print('%%%')
        if globals.g_workcolormode==1:
            self.cvworkjHmodeEdMustTop()
        elif globals.g_workcolormode==2: 
                self.cvworkjHmodeEdMust()
        elif globals.g_workcolormode==3: 
                self.cvwork()
        elif globals.g_workcolormode==4: 
                self.cvworkjHmodeEd()
    def cvworkapiwhile(self):
        self.cvworkRotApi()
    def cvworkRotApi(self):
        if globals.g_workcolormode==4:
            while self.cvworkjHmodeEd()==0:
                time.sleep(0.01)
        elif globals.g_workcolormode==3:
            while self.cvwork()==0:# cvwork
                time.sleep(0.01)
        elif globals.g_workcolormode==2:
            while self.cvworkjHmodeEdMust()==0:# 
                time.sleep(0.01)
        elif globals.g_workcolormode==1:
            while self.cvworkjHmodeEdMustTop()==0:# 
                time.sleep(0.01)
    def cvwork(self):
    
        total_seconds1 = time.time()
        #print("total_seconds1",total_seconds1)
        time_diff2 = (total_seconds1 - globals.gtotal_lastscreenseconds) * 1000
        if time_diff2<16:
            return 0
        globals.gtotal_lastscreenseconds=total_seconds1
        self.screenshot['left'] = int(self.scwith - (globals.g_fox / 2))
        self.screenshot['top'] = int(self.scheight - (globals.g_foy / 2))
        self.screenshot['width'] = globals.g_fox
        self.screenshot['height'] = globals.g_foy
        img = np.array(self.sct.grab(self.screenshot))

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.embaixo,self.emcima)
        kernel = np.ones((3,3), np.uint8)
        dilated = cv2.dilate(mask,kernel,iterations= 5)
        thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)# #CHAIN_APPROX_NONE
       
        if len(contours) != 0:
            num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh, connectivity=8)
            if num_labels==0:
                return 0
            #globals.g_tsleep=0.025
            #cv2.imwrite(f'./img/original_screenshot_{globals.G_intdex}.png', cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            #globals.G_intdex=globals.G_intdex+1
            # 建立并查集
            parent = list(range(num_labels))
            def find(x):
                if parent[x] != x:
                    parent[x] = find(parent[x])
                return parent[x]
            def union(x, y):
                parent[find(x)] = find(y)

            for c1 in range(1, num_labels):
                for c2 in range(c1+1, num_labels):
                    if self.are_close(stats[c1], stats[c2], centroids[c1], centroids[c2]):
                        union(c1, c2)

            color_map = {index: np.random.randint(0, 255, size=3) for index in range(1, num_labels)}
            color_map[0] = np.array([0, 0, 0])  # 设置背景色为黑色

            for c in range(1, num_labels):
                color_map[c] = color_map[find(c)]

            # 初始化一个全黑的彩色图片
            colored_image = np.zeros((*thresh.shape, 3), dtype=np.uint8)

            color_dict = {}

            for c in range(1, num_labels):
                y = centroids[c][1]
                color = tuple(color_map[c])
                if color in color_dict:
                    color_dict[color] = min(y, color_dict[color])
                else:
                    color_dict[color] = y
            if not color_dict: 
                return 0
            # 找出最上方的颜色

            top_color = min(color_dict, key=color_dict.get)

            for index, color in color_map.items():
                if tuple(color) == tuple(top_color):
                    colored_image[labels == index] = [0, 255, 0]  # green

            binary_image = cv2.inRange(colored_image, (0, 255, 0), (0, 255, 0))

            M = cv2.moments(binary_image)

            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                print("No green pixels found in the image")
                cX, cY = 0, 0
                return 0
            green_pixels = np.where(np.all(colored_image == [0, 255, 0], axis=-1))
            if green_pixels[0].size > 0:
                top_green_y = np.min(green_pixels[0])+3
                top_green_x = green_pixels[1][np.where(green_pixels[0] == top_green_y)[0][0]]
            else:
                print("No green pixels found in the image")
                return 0
            #计算需要移动到的距离
            i=self.scale_valueEx()

            top=(top_green_x,top_green_y)
            pixel=(cX, cY)
            px = pixel[0] 

            if globals.gissuiji==True:
                #随机瞄头
                total_seconds22 = time.time()
                time_dif22f = (total_seconds22 - globals.gtotal_lastgetpeople) * 1000  
                if time_dif22f>1000:#已经过去1秒新的人
                    if random.random() < 0.2:
                        globals.gctype=1
                    else:
                        globals.gctype=0
                globals.gtotal_lastgetpeople=total_seconds22
                if globals.gctype==0:
                    py = int(pixel[1] + (top[1] - pixel[1]) * i)
                else:
                    py=pixel[1]
            else:
                py = int(pixel[1] + (top[1] - pixel[1]) * i)

            aimzao=(px,py)
            distance=self.calculate_distanceEx(aimzao)
            if abs(distance[0])<4 and abs(distance[1])<4 :
                if globals.g_isshot:
                    total_secondsy = time.time()
                    time_diffy = (total_secondsy - globals.gtotal_lastshot) * 1000
                    if time_diffy<200:
                        pass
                    else:
                        globals.gtotal_lastshot=total_secondsy
                        serial_message = f"AT,ADBMV-3667,MO223,1\n"
                        globals.garduino.write(str.encode(serial_message))
                return 1

            isokcon,ty=self.istomoseyidong(aimzao[0],aimzao[1],distance)
            if isokcon==False:

                if globals.g_isshot:
                    total_secondsy = time.time()
                    time_diffy = (total_secondsy - globals.gtotal_lastshot) * 1000
                    if time_diffy<200:
                        pass
                    else:
                        globals.gtotal_lastshot=total_secondsy
                        serial_message = f"AT,ADBMV-3667,MO223,1\n"
                        globals.garduino.write(str.encode(serial_message))
                return 1
            
            self.lasdx=distance[0]+6332
            self.lasdy=distance[1]+10222
  

            serial_message = f"AT,ADBMV{self.lasdx},MO{self.lasdy},10003\n"
            #print(serial_message)
            globals.garduino.write(str.encode(serial_message))
            arduino_response = globals.garduino.readline() # 读取 arduino 的返回信号
            return 0
        else:#找不到人了sleep恢复
           #globals.g_tsleep=0.01
           return 1

    def cvworkjHmodeEd(self):
        #print('##')
        total_seconds = time.time()
        time_diff = (total_seconds - globals.gtotal_lastscreenseconds) * 1000
        if time_diff<16:
            return 0
        #print('#####001',time_diff)
        globals.gtotal_lastscreenseconds=total_seconds

        self.screenshot['left'] = int(self.scwith - (globals.g_fox / 2))
        self.screenshot['top'] = int(self.scheight - (globals.g_foy / 2))
        self.screenshot['width'] = globals.g_fox
        self.screenshot['height'] = globals.g_foy
        img = np.array(self.sct.grab(self.screenshot))

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.embaixo,self.emcima)
        kernel = np.ones((2,3), np.uint8)
        dilated = cv2.dilate(mask,kernel,iterations= 3)
        thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)# #CHAIN_APPROX_NONE
    
        if len(contours) != 0:

            screen_center = (globals.g_fox // 2, globals.g_foy // 2)
            min_distance = float('3000.0')
            closest_contour = None

            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                center = (x + w // 2, y + h // 2)
                distance = ((center[0] - screen_center[0]) ** 2 + (center[1] - screen_center[1]) ** 2) ** 0.5

                if distance < min_distance:
                    min_distance = distance
                    closest_contour = contour
            if closest_contour is None:
                return 0

            x, y, w, h = cv2.boundingRect(closest_contour)
            M = cv2.moments(closest_contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                cX= x + w // 2
                cY= y+3


            i=self.scale_valueEx()
            tX = x + w // 2
            ty=y+3
            top=(tX,ty)
            pixel=(cX, cY)
           # px = pixel[0] 
           # py = int(pixel[1] + (top[1] - pixel[1]) * i)
            vector = np.array(pixel) - np.array(top)  # 连接 top 点和 pixel 点的方向向量
            interpolated_point = np.array(top) + (1 - i) * vector  # 插值点的坐标

            px = int(interpolated_point[0])
            py = int(interpolated_point[1]) 


            aimzao=(px,py)
            distance=self.calculate_distanceEx(aimzao)
            if abs(distance[0])<3 and abs(distance[1])<3 :
                #time.sleep(0.005)
                if globals.g_isshot:
                    total_secondsy = time.time()
                    time_diffy = (total_secondsy - globals.gtotal_lastshot) * 1000
                    if time_diffy<200:
                        pass
                    else:
                        globals.gtotal_lastshot=total_secondsy
                        serial_message = f"AT,ADBMV-3667,MO223,1\n"
                        globals.garduino.write(str.encode(serial_message))
                return 1
            '''
            isokcon,ty=self.istomoseyidongEx(x,x+w,y,y+h,aimzao[0],aimzao[1],distance)
            if isokcon==False:
                if globals.g_isshot:
                    total_secondsy = time.time()
                    time_diffy = (total_secondsy - globals.gtotal_lastshot) * 1000
                    if time_diffy<200:
                        pass
                    else:
                        globals.gtotal_lastshot=total_secondsy
                        serial_message = f"AT,ADBMV-3667,MO223,1\n"
                        globals.garduino.write(str.encode(serial_message))
                return 1
            '''
            #print(distance)
            self.lasdx=distance[0]+6332
            self.lasdy=distance[1]+10222
            
            serial_message = f"AT,ADBMV{self.lasdx},MO{self.lasdy},10003\n"


            globals.garduino.write(str.encode(serial_message))
            arduino_response = globals.garduino.readline() # 读取 arduino 的返回信号
            return 0
        else:
            return 1
    def cvworkjHmodeEdMust(self):
        #移动到最近的
        #再找最上面的
         #print('##')
        total_seconds = time.time()
        time_diff = (total_seconds - globals.gtotal_lastscreenseconds) * 1000
        if time_diff<16:
            return 0
        #print('#####001',time_diff)
        globals.gtotal_lastscreenseconds=total_seconds

        total_seconds22 = time.time()
        time_dif22f = (total_seconds22 - globals.gtotal_lastgetpeople) * 1000  
        if time_dif22f>1000:#已经过去1.5秒新的人
            globals.gistotop=False
        if  globals.gistotop==False:
            self.screenshot['left'] = int(self.scwith - (globals.g_fox / 2))
            self.screenshot['top'] = int(self.scheight - (globals.g_foy / 2))
            self.screenshot['width'] = globals.g_fox
            self.screenshot['height'] = globals.g_foy
        else:
            self.screenshot['left'] = int(self.scwith - ( globals.g_topfox / 2))
            self.screenshot['top'] = int(self.scheight - (globals.g_foy / 2))
            self.screenshot['width'] = globals.g_topfox
            self.screenshot['height'] = globals.g_foy
        img = np.array(self.sct.grab(self.screenshot))

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.embaixo,self.emcima)
        kernel = np.ones((2,3), np.uint8)
        dilated = cv2.dilate(mask,kernel,iterations= 3)
        thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)# #CHAIN_APPROX_NONE
    
        if len(contours) != 0:



            globals.gtotal_lastgetpeople=total_seconds22
            
            closest_contour = None
            

            if  globals.gistotop==False:
                min_distance = float('600.0')
                screen_center = (globals.g_fox // 2, globals.g_foy // 2)
                for contour in contours:
                    x, y, w, h = cv2.boundingRect(contour)
                    center = (x + w // 2, y + h // 2)
                    distance = ((center[0] - screen_center[0]) ** 2 + (center[1] - screen_center[1]) ** 2) ** 0.5

                    if distance < min_distance:
                        min_distance = distance
                        closest_contour = contour
            else:
                min_y = float('600.0')
                for contour in contours:
                    x, y, w, h = cv2.boundingRect(contour)
                    #print(x, y, w, h )
                    if y < min_y:
                        min_y = y
                        closest_contour = contour

            if closest_contour is None:
                print('closest_contour is None')
                return 0
            x, y, w, h = cv2.boundingRect(closest_contour)
            M = cv2.moments(closest_contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                cX= x + w // 2
                cY= y


            i=self.scale_valueEx()
            tX = x + w // 2
            ty=y
            top=(tX,ty)
            pixel=(cX, cY)

            vector = np.array(pixel) - np.array(top)  # 连接 top 点和 pixel 点的方向向量
            interpolated_point = np.array(top) + (1 - i) * vector  # 插值点的坐标

            px = int(interpolated_point[0])
            py = int(interpolated_point[1]) 


            aimzao=(px,py)
            distance=self.calculate_distanceExD(aimzao)
            if abs(distance[0])<3 and abs(distance[1])<3 :
                reti=1
                if  globals.gistotop==False:
                      globals.gistotop=True
                      reti=0
                      print('#######')
                if globals.g_isshot and globals.gistotop==True:
                    total_secondsy = time.time()
                    time_diffy = (total_secondsy - globals.gtotal_lastshot) * 1000
                    if time_diffy<200:
                        pass
                    else:
                        globals.gtotal_lastshot=total_secondsy
                        serial_message = f"AT,ADBMV-3667,MO223,1\n"
                        globals.garduino.write(str.encode(serial_message))

                return reti
            #print(distance)
            self.lasdx=distance[0]+6332
            self.lasdy=distance[1]+10222
            random_integer = random.randint(400, 800)
            if  globals.gistotop==True:
                #serial_message = f"AT,ADBMV{self.lasdx},MO{self.lasdy},-1\n"
               # serial_message = f"AT,ADBMV{self.lasdx},MO{self.lasdy},{random_integer}\n"
                serial_message = f"AT,ADBMV{self.lasdx},MO{self.lasdy},10005\n"
            else:
                serial_message = f"AT,ADBMV{self.lasdx},MO{self.lasdy},10003\n"
                #serial_message = f"AT,ADBMV{self.lasdx},MO{self.lasdy},{random_integer}\n"

            globals.garduino.write(str.encode(serial_message))
            arduino_response = globals.garduino.readline() # 读取 arduino 的返回信号
            return 0
        else:

            return 2            
    def cvworkjHmodeEdMustTop(self):

        total_seconds = time.time()
        time_diff = (total_seconds - globals.gtotal_lastscreenseconds) * 1000
        if time_diff<16:
            return 0

        globals.gtotal_lastscreenseconds=total_seconds
      
        self.screenshot['left'] = int(self.scwith - (globals.g_fox / 2))
        self.screenshot['top'] = int(self.scheight - (globals.g_foy / 2))
        self.screenshot['width'] = globals.g_fox
        self.screenshot['height'] = globals.g_foy

        img = np.array(self.sct.grab(self.screenshot))

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.embaixo,self.emcima)
        kernel = np.ones((2,3), np.uint8)
        dilated = cv2.dilate(mask,kernel,iterations= 3)
        thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)# #CHAIN_APPROX_NONE
    
        if len(contours) != 0:

            closest_contour = None
            min_y = float('600.0')
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                #print(x, y, w, h )
                if y < min_y:
                    min_y = y
                    closest_contour = contour
            if closest_contour is None:
                print('closest_contour is None')
                return 0
            x, y, w, h = cv2.boundingRect(closest_contour)
            M = cv2.moments(closest_contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                cX= x + w // 2
                cY= y

            i=self.scale_valueEx()
            tX = x + w // 2
            ty=y
            top=(tX,ty)
            pixel=(cX, cY)

            vector = np.array(pixel) - np.array(top)  # 连接 top 点和 pixel 点的方向向量
            interpolated_point = np.array(top) + (1 - i) * vector  # 插值点的坐标

            px = int(interpolated_point[0])
            py = int(interpolated_point[1]) 
            aimzao=(px,py)
            distance=self.calculate_distanceEx(aimzao)
            if abs(distance[0])<3 and abs(distance[1])<3 :
                reti=1
                if globals.g_isshot :
                    total_secondsy = time.time()
                    time_diffy = (total_secondsy - globals.gtotal_lastshot) * 1000
                    if time_diffy<200:
                        pass
                    else:
                        globals.gtotal_lastshot=total_secondsy
                        serial_message = f"AT,ADBMV-3667,MO223,1\n"
                        globals.garduino.write(str.encode(serial_message))
                return reti

            self.lasdx=distance[0]+6332
            self.lasdy=distance[1]+10222
           # random_integer = random.randint(200, 400)
           # serial_message = f"AT,ADBMV{self.lasdx},MO{self.lasdy},{random_integer}\n"
            serial_message = f"AT,ADBMV{self.lasdx},MO{self.lasdy},10003\n"
            globals.garduino.write(str.encode(serial_message))
            arduino_response = globals.garduino.readline() # 读取 arduino 的返回信号
            return 0
        else:
            return 2           