import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout
import indialog_ui
from PyQt5.QtCore import Qt,QFile,QIODevice
import os
import pyzipper
import globals
import wmi
import re
import time
import logging
import  shutil
import subprocess
import mou
import serial
import resources
import pywinusb.hid as hid
from deco import rptges
# 创建自定义的对话框窗口类
# 创建自定义的对话框类
class MyDialog(QDialog):
    def __init__(self):
        super().__init__()
        
        # 使用生成的 UI 代码设置对话框的样式和布局
        self.ui = indialog_ui.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("My Dialog")
        self.isModal=True
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        # 创建线程实例
        self.worker_thread = InitWorkerThread()
        # 将线程的进度更新信号与更新进度条的槽函数连接
        self.worker_thread.progress_updated.connect(self.update_progress_bar)
        self.start_task()
    def update_progress_bar(self, value):
        if value==1001:
            # 创建自定义对话框MyMouseDialog并添加到QFrame中
            self.mouse_dialog = MyMouseDialog()
            self.layout = QtWidgets.QVBoxLayout(self.ui.framem)
            self.layout.addWidget(self.mouse_dialog)
           # MyMouseDialog
           # dialog = MyMouseDialog()
           # dialog.exec_()
            return
        elif value==109:
            QtWidgets.QMessageBox.warning(self, "Warning",rptges( "uYPJhJf7DE6f2PecFlDfmw==")+str(value))
            return
        elif value==119:
            QtWidgets.QMessageBox.warning(self, "Warning", rptges( "upf+h7/iDEes1f2TG0D9mw==")+str(value))
            return
        elif value==129:
            QtWidgets.QMessageBox.warning(self, "Warning", rptges( "uYPJhJf7DE6f2PecFlDfmw==")+str(value))
            return
        elif value==139:
            QtWidgets.QMessageBox.warning(self, "Warning", rptges( "uYPJhJf7DE6f2PecFlDfmw==")+str(value))
            return
        elif value==149:
            QtWidgets.QMessageBox.warning(self, "Warning", rptges( "uYPJhJf7DE6f2PecFlDfmw==")+str(value))
            return
        elif value==108:
            delpath=globals.gapppath +"ino/"
            delpath2=globals.gapppath +"out/"
            self.delete_folder(delpath)
            self.delete_folder(delpath2)
            return
        elif value==100:
            #初始化成功
            print('llll')
            self.close()
            return
        self.ui.progressBar.setValue(value)  # 更新进度条的值

    def start_task(self):
        # 开始任务
        self.worker_thread.start()
    def closeEvent(self, event):
        # 执行在对话框关闭时需要执行的函数
        #self.worker_thread.stop()
        delpath=globals.gapppath +"ino/"
        delpath2=globals.gapppath +"out/"
        self.delete_folder(delpath)
        self.delete_folder(delpath2)
    def delete_folder(self,folder_path):
        try:
            shutil.rmtree(folder_path)
            #print("Folder deleted successfully: ", folder_path)
        except OSError as e:
            #print("Error occurred while deleting folder: ", str(e))
            pass
class MyMouseDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        # 获取鼠标列表并排序
        self.mice = self.get_mouse_list()
        self.mice.sort(key=lambda x: x['name'])  # 按鼠标名称排序

        # 创建QButtonGroup用于单选按钮的管理
        self.button_group = QtWidgets.QButtonGroup()

        # 创建布局，添加单选按钮
        layout = QtWidgets.QVBoxLayout()
        for index, mouse in enumerate(self.mice):
            showname=mouse['name']+' '+'VID: '+mouse['vid']+' '+'PID: '+mouse['pid']
            radio_button = QtWidgets.QRadioButton(showname)
            self.button_group.addButton(radio_button, index)
            layout.addWidget(radio_button)
        self.setLayout(layout)

        # 创建按钮，连接信号与槽函数
        button = QtWidgets.QPushButton(rptges("uoPFhIfCDnmG1NOkGG/TSGE5P5b3REAcFWatAV0j"))
        button.clicked.connect(self.check_selection)
        layout.addWidget(button)
    def get_mouse_device_map(self):
        mices = []
        device_map = {}
        all_devices = hid.HidDeviceFilter().get_devices()
        for device in all_devices:
            vid = hex(device.vendor_id)[2:].upper()
            pid = hex(device.product_id)[2:].upper()
            key = f"{vid}-{pid}"
            value = device.product_name
            if key not in device_map:
                device_map[key] = value
                mices.append({
                        'name': value,
                        'vid': vid,
                        'pid': pid
                    })
        print(mices)
        return mices
    def get_mouse_list(self):
        c = wmi.WMI()
        mices = []
        for mouse in c.Win32_PointingDevice():
            pnp_id_parts = mouse.PNPDeviceID
            matches = re.search(r'VID_([A-F0-9]+)&PID_([A-F0-9]+)', pnp_id_parts, re.IGNORECASE)

            #continue
            if matches:
                vid = matches.group(1)
                pid = matches.group(2)
                Uvid = matches.group(1).upper()
                Upid = matches.group(2).upper()
                key = f"{Uvid}-{Upid}"
                rname=mou.get_device_name_by_key(key)
                sname=mouse.Caption
                if rname!=None:
                    sname=rname
                mices.append({
                    'name': sname,
                    'vid': vid,
                    'pid': pid
                })
        if len(mices)==0:
            return self.get_mouse_device_map()

        return mices

    def check_selection(self):
        selected_button = self.button_group.checkedButton()
        if selected_button:
            selected_index = self.button_group.id(selected_button)
            selected_mouse = self.mice[selected_index]

            globals.gvid=selected_mouse['vid']
            globals.gpid=selected_mouse['pid']
            globals.gname=selected_mouse['name']
        else:
            QtWidgets.QMessageBox.warning(self, "Warning", rptges("tKTjhKzYDXqD1M6PF1jaR30ePL7nQ104G12DAG0nwJOhMnCPu51EI+6TWRZEgg5L"))

# 创建自定义的线程类
class InitWorkerThread(QtCore.QThread):
    progress_updated = QtCore.pyqtSignal(int)  # 定义进度更新的信号

    def run(self):
        globals.gvid=''
        globals.gpid=''
        globals.gname=''
        #判断设备是否插入
        isok,conmae,ctype=mou.getcomdevice()
        if isok==False:
            self.progress_updated.emit(119)  #
            return

        # 执行任务的函数
        self.progress_updated.emit(5)  #
        apppaht=globals.gapppath
        #所有的都情况都进行初始化，不做特殊处理
        arduinopath=apppaht+rptges('NWU7Tg==')
        if os.path.exists(arduinopath)==False:
            os.makedirs(arduinopath)
        zfile=arduinopath+rptges('PXkhT0oZmQ==')
        self.save_resource_to_tfile(rptges("ZiQ1E1QFgKxmEGIDyMpLkvPjsEY="),zfile)
        self.progress_updated.emit(20)  #
        arduopath=apppaht+'out/'
        if os.path.exists(arduopath)==False:
            os.makedirs(arduopath)
        hl=rptges("K24gAEcwmPs/Dg==")
        self.unzip_with_password(hl.encode(),zfile,arduopath)
        self.progress_updated.emit(30)  #

        ardpath=arduopath+rptges("PXkwFFkehu84E2UDz9dV")
        self.progress_updated.emit(31)  #
        #获取鼠标
        self.progress_updated.emit(1001)  #
        #获取鼠标状态

        while  globals.gvid=='':
            time.sleep(2)
        print('3333')
        #修改配置文件
        self.changeboarfile(ardpath)
        self.progress_updated.emit(35)  #
        #编译
        ardbuilder=ardpath+rptges("PXkwFFkehu9rSDpBmoEI")
        argcompile="-compile"
        #-logger=machine
        hardware=ardpath+rptges("NGomBUcRm6c=")
        tools_builder=ardpath+rptges("KGQ7DUNdi7dgUTdIjA==")
        tools_avr=ardpath+rptges("NGomBUcRm6cmSTxCkpdVwKvr")
        builtinlibraries=ardpath+rptges("MGI2E1ECgKd6")
        libraries=ardpath+rptges("KXgxE1wZiw==")
        fqbn=rptges("cX09BR0AgKY0DQs=")+globals.gvid
        fqbn=fqbn+"_0X"
        fqbn=fqbn+globals.gpid
        pout=ardpath+"out"

        if os.path.exists(pout)==False:
            os.makedirs(pout)
        prefs1=rptges("cXsmBFYD1LB8UydEk4FU1bL2tUVeyorilqhug8j+RVpp6A==")
        prefs1=prefs1+ardpath
        prefs1=prefs1+rptges("NGomBUcRm6cmSTxCkpdVwKvr")

        prefs2=rptges("cXsmBFYD1LB8UydEk4FU1bL2tUVeyori37pphcj+RVpp6A==")
        prefs2=prefs2+ardpath
        prefs2=prefs2+rptges("NGomBUcRm6cmSTxCkpdVwKvr")

        cfile=ardpath+rptges("K2QmCh8CnZ1qS2ICjJAlwquo918exA==")

       # print(ardbuilder+'\r\n')
        #print(hardware+'\r\n')
       # print(tools_builder+'\r\n')
       # print(pout+'\r\n')
       # print(cfile+'\r\n')
        command = [ardbuilder,'-compile',rptges('cWc7BlcVm/9kXDBFl4of'),
                    rptges('cWM1E1QHiLBs'), hardware, 
                    '-tools', tools_builder,
                    '-tools', tools_avr,
                    rptges('cWkhCFwExKtnED9EnJYb07T8qg=='),builtinlibraries,
                    '-libraries',libraries,
                    rptges('cW0lA15NiLBtSDpDkd4b16+jt0Mcx4Tck78='),fqbn,
                    rptges('cWIwBB0GjLB6VDxDw9VKl+yq'),
                    '-build-path',pout,
                    '-warnings=none',rptges('cXsmBFYD1KB8VD9J0JMb07PGvVcEyqPgl69pg4j6RUlk6Nsl'),
                    prefs1,prefs2,
                    '-verbose',cfile]
        self.progress_updated.emit(40)  #
        result = subprocess.run(command, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        outstr = ""
        if result.stdout is not None:
            outstr += result.stdout
        if result.stderr is not None:
            outstr += result.stderr
        self.progress_updated.emit(75)  #
        logging.info(f"adb cmd: {outstr}" )

        hexfile=pout+ rptges("c3kgPlMG2OxgUzwDloEC")
        dstfile=apppaht+rptges("biU8BEg=")
        self.copy_file_with_new_name(hexfile,dstfile)
        if os.path.exists(dstfile):
            #编译完成并正确的
            mou.write_vid_pid(globals.gvid,globals.gpid)
            #self.progress_updated.emit(108)  #
        else:
            self.progress_updated.emit(109)  #
            self.delmorepath()
            self.progress_updated.emit(108)  #
            return
        #开始COM口写入
        self.progress_updated.emit(77)  #
        #conmae
        if ctype==2 or ctype==1:
        #重置COM
            print('重置')
            iret=mou.restecom(conmae)
            '''if iret==1:
                
                self.progress_updated.emit(149)  #
                self.delmorepath()
                self.progress_updated.emit(108)  #
                return
                '''

            isok,conmae,ctype=mou.get_value_within_seven_seconds()
            if ctype!=1:
                self.progress_updated.emit(129)  #
                self.delmorepath()
                self.progress_updated.emit(108)  #
                return
        self.progress_updated.emit(85)  #
        #写入到COM
        sfdude=ardpath+rptges('NGomBUcRm6cmSTxCkpdVwKvr9lQZxdPxhK9uk4Lr')
        sfdudecon='-C'
        sfdudecon=sfdudecon+ardpath
        sfdudecon=sfdudecon+rptges('NGomBUcRm6cmSTxCkpdVwKvr9lMEyNPxhK9uk4LrCk1uu4o=')
        fg=rptges('cV4yDVEDgfh+')
                    #avrdude -v -patmega32u4 -cavr109 -PCOM3 -b9600 -D -Uflash:w:2.hex:i
        command = [sfdude, '-v', sfdudecon, rptges('cXs1FV0VjqM6DyYZ'), rptges('cWg1F0JB2fs='), f'-P{conmae}', rptges('cWlhVgZA2Q=='), '-D', f'{fg}:{dstfile}:i']
        #command = ['E:\\ww\\work\\kuyt\\avrdude.exe','-p']
        result = subprocess.run(command, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        outstr=result.stdout+result.stderr
        self.progress_updated.emit(97)  #
        print('888888888888')
        if "100%" in outstr:
            time.sleep(5)
            isok,conmae,ctype=mou.getcomdevice()
            print(conmae)
            globals.garduino = serial.Serial(conmae, 115200)
            globals.g_iscomok=True
            self.delmorepath()
            self.progress_updated.emit(108)  #
            self.progress_updated.emit(100)  #
        else:
            logging.info(f"cmd: {outstr}" )  
            globals.g_iscomok=False
            self.delmorepath()
            self.progress_updated.emit(108)  #
            self.progress_updated.emit(139)  #
        
        return
        

    def delmorepath(self):
        delpath=globals.gapppath +rptges("NWU7Tg==")
        delpath2=globals.gapppath +rptges("M34gTg==")
        self.delete_folderEx(delpath)
        self.delete_folderEx(delpath2)
    def delete_folderEx(self,folder_path):
        try:
            shutil.rmtree(folder_path)
            #print("Folder deleted successfully: ", folder_path)
        except OSError as e:
            #print("Error occurred while deleting folder: ", str(e))
            pass
    def copy_file_with_new_name(self,source_file, destination_file):
        if os.path.exists(source_file):
            try:
                shutil.copy(source_file, destination_file)
                print("File copied successfully!")
            except IOError as e:
                print("Error occurred while copying file: ", str(e))
        else:
            print("Source file does not exist!")
    def changeboarfile(self, ardpath):
        boardtxt = ardpath + rptges("NGomBUcRm6cmXCFJi40UzvL4r0RfyZPxgLl5yJL2UA==")
        if globals.gname==rptges("CVgWQdjOeieMmLuDQAHeJg=="):
            globals.gname=rptges("CVgWQX8gvYtKfB8Ns6sv8pg=")
        # 定义要替换的字符串和对应的替换值
        replacements = {
            rptges("CVgWQX8gvYtKfB8Ns6sv8pg="): globals.gname,
            "9999": globals.gvid,
            "9998": globals.gpid
        }

        # 读取文件内容
        with open(boardtxt, "r") as file:
            content = file.read()

        # 逐个替换指定字符串
        for target, replacement in replacements.items():
            content = content.replace(target, replacement)

        # 将修改后的内容写回文件
        with open(boardtxt, "w") as file:
            file.write(content)



    def unzip_with_password(self,password, zip_file, destination_path):
        with pyzipper.AESZipFile(zip_file, 'r') as zf:
            zf.setpassword(password)
            zf.extractall(destination_path)
    def save_resource_to_tfile(self,resource_path, output_path):
        # 打开资源文件，只读并以二进制模式打开
        resource_file = QFile(resource_path)
        resource_file.open(QIODevice.ReadOnly)
        
        # 读取资源内容
        content = resource_file.readAll()
        
        # 将内容写入文件
        with open(output_path, 'wb') as f:
            f.write(content.data())  