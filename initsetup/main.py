from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt,QEvent
from PyQt5.QtWidgets import QSlider
import globals  # 导入包含全局变量的模块
import logging
import cvwindow_ui
import mou
from PyQt5.QtCore import QTimer
from initdev import InitDev
from datetime import datetime
from deco import rptges
from inmain import MyDialog
import wmi
import os
import subprocess

class MyWindow(QtWidgets.QMainWindow, cvwindow_ui.Ui_MTU):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.inpushButton.clicked.connect(self.init_work)
        self.inpushButton.setEnabled(False)
        self.labelinfo.setText(rptges('uqjUh6/VDkym2PGuGlzXSXIuPp79Tmwe'))
        # 连接复选框状态改变事件到处理函数
        if os.path.exists('11.txt'):
            logging.basicConfig(filename='ll.log', level=logging.INFO,
                format='%(asctime)s %(levelname)s: %(message)s', 
                datefmt='%Y-%m-%d %I:%M:%S')
        else:
            print('File does not exist')
            logging.basicConfig(filename='ll.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s: %(message)s', 
                    datefmt='%Y-%m-%d %I:%M:%S')
        globals.gwmihead = wmi.WMI()
        globals.gmousemap=mou.get_mouse_device_map()
        #初始化的进程
        self.InitDever= InitDev(self.is_checkbox_checked,self) 
        self.InitDever.update_signal.connect(self.on_update_signal)
        self.InitDever.start()
    def is_checkbox_checked(self, value):
            pass
    def eventFilter(self, obj, event):
        if isinstance(obj, QSlider) and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Home:
                return True  # 拦截Home键事件
        return super().eventFilter(obj, event)

    def on_update_signal(self, value):
        print("on_update_signal value:",value)
        if value==3:
            print('###########',value)
            self.controlradio(0)
        elif value==4:
            self.controlradio(1)
        elif value==6:#初始化成功
            self.labelinfo.setText(rptges('uqbwMXOVXnDstc7IWW+fLUt2ZbqYBEt3aWnsaENqmZHmQUT42qk8WNg='))
            self.inpushButton.setEnabled(True)
        elif value==5:
            self.labelinfo.setText(rptges('uqb3hKzYDEip1e6QHWT4Ql0bOrby'))#rptges '正在加载。。。'
        elif value==9:
            self.labelinfo.setText(rptges('upf+h7nODEq51f2TG0D9TmEVMZnHTXMCF1ivDkgwwYqGMFWmu7tHIdOcVSZyixJAImfVfgLNfgxpmgB9OeIboQ6U1Pqu'))#'No  Leonardo'
        elif value==10:
            self.labelinfo.setText(rptges('HXkwFFkehuJcTT9Cn4Ba5K/rtkQ='))
        elif value==91:
            self.labelinfo.setText(rptges('upf+hLjtDGWC2N+7EVj2SXIuP7niTnk1GnO0A0IJwb6PMGSNu5RRIfiBXxZogyB8IHXNfybofztLmBt6McoyoQ6U1Pqu'))
            self.inpushButton.setEnabled(True)
        elif value==92:
            self.labelinfo.setText(rptges('tKTjh7/iDEes1f2TG0D9RE0XPrTJTnsrF1WXA0EFwaKXOlCcub1qIei/VBJpgSFjIn3NdCLkdQhlkDNT'))
            self.inpushButton.setEnabled(True)
        elif value==94:
            self.labelinfo.setText(rptges('tKbyhKH6Bn6T29GFGX7+SXMnPJL3TlEIF0GiA0IUwJarPFCwuJNdK8ibVyRLgQxPIVHofjDsfzFM'))
            self.inpushButton.setEnabled(True)
        elif value==95:
            self.labelinfo.setText(rptges('tKbyhKH6Bn6T29GFGX7+SXMnPJL3TksiFWaFDkQlwau3MVeGtrdAIui7VSJ5gQlHIGXzcyHidQholyBlN/E+qCSl3s6ygqbEh+ky'))
            self.inpushButton.setEnabled(True)
    def init_work(self):
        if globals.g_iscomok==True:
            msgBox = QtWidgets.QMessageBox()
            # 设置消息框在父级窗口之上
            msgBox.setWindowFlags(msgBox.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
            msgBox.setWindowTitle("Warning")
            msgBox.setText(rptges("ubzmhov/DEqU2PSmG2jsTmEVMZnHT0QdGnuLD2EDwYqMMGSNu5RRIfiBVBdEgzRIlaqKJxKCIRMDxCI3UdlbzQ/xh9zKyL2n5dFCAzbll/rj5sODAyM="))
            continue_button = msgBox.addButton(rptges("uoPFiZbxDnmu2uiAG2znRHoSPLrm"), QtWidgets.QMessageBox.ButtonRole.ActionRole)
            terminate_button = msgBox.addButton(rptges("u7Dch53S"), QtWidgets.QMessageBox.ButtonRole.RejectRole)
            msgBox.exec()
            if msgBox.clickedButton() == continue_button:
                # 继续按钮被点击
                print("Continue button clicked")
                # 在这里添加继续按钮被点击后的逻辑

            elif msgBox.clickedButton() == terminate_button:
                # 终止按钮被点击
                print("Terminate button clicked")
                # 在这里添加终止按钮被点击后的逻辑
                return
        dialog = MyDialog()
        dialog.exec_()
        if globals.g_iscomok==True:
            self.labelinfo.setText(rptges('uqbwMXOVXnDstc7IWW+fLUt2ZbqYBEt3aWnsaENrtIHkX0Q='))
def delete_self_in(sec=5):
    script = f"""
    @echo off
    timeout /t {sec} /nobreak > nul
    del "%~f0"
    """
    with open('delete_self.bat', 'w') as f:
        f.write(script)
    subprocess.Popen('delete_self.bat')
   
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    ui = MyWindow()
    ui.show()
    sys.exit(app.exec_())