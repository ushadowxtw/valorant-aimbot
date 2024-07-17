from PyQt5.QtCore import QThread, pyqtSignal,QTime
import globals 
import time
import os
import serial
from serial.tools import list_ports
import logging
from deco import rptges
import mou
from PyQt5 import QtWidgets, QtCore, QtGui
class InitDev(QtCore.QThread):
    check_status = pyqtSignal()
    update_signal = pyqtSignal(int)

    def __init__(self, callback, parent=None):
        super().__init__(parent)
        self.check_callback = callback
        self.lnumb=mou.getmousenumber()
        appdata_path = os.getenv(rptges('HVsEJXEkqA=='))
        appdata_path=appdata_path+rptges("c2okER9eiLB/Eg==")
        globals.gapppath=appdata_path
        if os.path.exists(appdata_path)==False:
            os.makedirs(appdata_path)
        globals.gfilehex=appdata_path+rptges("biU8BEg=")
        globals.gfileinit=appdata_path+rptges("biU9D1kE")
        self.isooof=mou.checkmouseisok()
    def run(self):
        #检查鼠标和hex文件
        if os.path.exists(globals.gfileinit) and os.path.exists(globals.gfilehex):
            print("File exists.")
        else:
            self.update_signal.emit(91)
            return
        print('############################################')
       
        print('############################################')
        if self.lnumb==1:
            self.update_signal.emit(92)
            return
        elif self.lnumb>2:
            self.update_signal.emit(94)
                    
        if self.isooof==False:
            print('is 91')
            self.update_signal.emit(91)
            return
        
        isok=False
        #找到COM口
        ports = list_ports.comports()
        for port, desc, hwid in sorted(ports):
            print(f"{port}: {desc}")
            logging.info(f"{port}: {desc}")  
            if rptges("CVgWQdTIWyqosbuDQAHeJg==") in desc:
                #找到了串行设备
                try:
                    with serial.Serial(port, 115200, timeout=5) as cyt:
                        serial_message =rptges( "HV94IHQypI0kDmUYyMg39/Cg4A9Jh87MnA==")#"AT,MO-3656,MV-9999,2\n"

                        cyt.write(str.encode(serial_message))
                        arduino_response = cyt.readline().decode().strip()
                        print(" arduino_response",arduino_response)
                        if rptges("FXh0Dls=") in arduino_response:
                            # 连接成功
                            isok=True
                            globals.garduino=cyt
                            globals.g_iscomok=True
                            globals.gcomename=port
                            cyt.close()

                            break
                        else:
                            cyt.close() #设置超时
                except (serial.SerialException, serial.serialutil.SerialTimeoutException, ValueError) as e:
                    # 发生异常，关闭串口连接并处理异常
                    if isinstance(e, ValueError):
                        print(" not received")
                    else:
                        print(" error:", str(e))
                #发送验证信息
        if globals.g_iscomok==True:
            globals.garduino = serial.Serial(globals.gcomename, 115200)
            self.update_signal.emit(6)
        else:
            self.update_signal.emit(95)



       