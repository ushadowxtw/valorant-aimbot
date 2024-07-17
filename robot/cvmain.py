from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QDoubleValidator,QIntValidator
from PyQt5.QtCore import Qt,QFile,QIODevice,QEvent

from PyQt5.QtWidgets import QSlider
from PIL import Image
import globals  
import logging
import keyboard
import cvwindow_ui
import mou
from PyQt5.QtCore import QTimer
from worker import Worker  
from keyboardthread import KeyBoardWorker
from mousethread import MouseWorker
from initdev import InitDev
from datetime import datetime
import mouse
from ctypes import windll
from deco import rptges
import wmi
import os
class MyWindow(QtWidgets.QMainWindow, cvwindow_ui.Ui_APP):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
   
        screen = QApplication.desktop().screenGeometry()
   
        x, y =screen.width()-self.width() - 100, screen.height() - self.height() - 300

        self.move(x, y)
        self.resize(656,350)
        self.isshow=True
        validator = QDoubleValidator(0.1, 10, 1) 
        self.lineEdit.setValidator(validator)




        self.hverticalSlider.valueChanged.connect(self.hupdate_label)
        self.mshorizontalSlider.valueChanged.connect(self.msupdate_label)


        self.hverticalSlider.installEventFilter(self)
        self.mshorizontalSlider.installEventFilter(self)
        self.pushButton.clicked.connect(self.copy_text)
        self.spushButton.clicked.connect(self.setxy_text)
        self.inpushButton.clicked.connect(self.init_work)
        self.startpushButton.clicked.connect(self.start_work)
        self.startpushButton.hide()
        self.inpushButton.setEnabled(False)
        self.labelinfo.setText(rptges("uqjUh6/VDkym2PGuGlzXSXIuPp79Tmwe"))
   
        self.shotcheckBox.stateChanged.connect(self.handle_checked)
        self.yqcheckBox.stateChanged.connect(self.yasqing_checked)

        self.ancheckBox.stateChanged.connect(self.anhandle_checked)
        self.suijicheckBox.stateChanged.connect(self.suijihandle_checked)
        validator = QIntValidator(1, 600)  
        self.xlineEdit.setValidator(validator) 
        self.ylineEdit.setValidator(validator) 
        self.xlineEdit.setText(str(globals.g_fox))
        self.ylineEdit.setText(str(globals.g_foy))



        self.lineEdit.setText(str(globals.g_mouspeed))
  
        self.radioButton1.toggled.connect(lambda checked: self.onRadioButtonChecked(checked, 1))
        self.radioButton2.toggled.connect(lambda checked: self.onRadioButtonChecked(checked, 2))
        self.radioButton3.toggled.connect(lambda checked: self.onRadioButtonChecked(checked, 3))
        self.radioButton4.toggled.connect(lambda checked: self.onRadioButtonChecked(checked, 4))
        self.radioButton5.toggled.connect(lambda checked: self.onRadioButtonChecked(checked, 5))
        self.radioButton6.toggled.connect(lambda checked: self.onRadioButtonChecked(checked, 6))


        self.radioButtonmod1.toggled.connect(lambda checked: self.onRadioButtonModChecked(checked, 1))
        self.radioButtonmod2.toggled.connect(lambda checked: self.onRadioButtonModChecked(checked, 2))
        self.radioButtonmod3.toggled.connect(lambda checked: self.onRadioButtonModChecked(checked, 3))
        self.radioButtonmod4.toggled.connect(lambda checked: self.onRadioButtonModChecked(checked, 4))


        if os.path.exists('1.txt'):
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

        self.suijicheckBox.setVisible(False)
        self.frame_13.setVisible(False)
        self.frame_11.setVisible(False)
        self.inpushButton.setVisible(False)
        self.line_5.setVisible(False)
        self.radioButton6.setVisible(False)
       
        self.InitDever= InitDev(self.is_checkbox_checked,self) 
        self.InitDever.update_signal.connect(self.on_update_signal)
        self.InitDever.start()

        self.worker = Worker(self.is_checkbox_checked) 
        self.worker.update_signal.connect(self.on_update_signal)
        self.worker.start()
        #
        '''
        self.KeyBoardWorker = KeyBoardWorker(self.is_checkbox_checked) 
        self.KeyBoardWorker.update_signal.connect(self.on_update_signal)
        self.KeyBoardWorker.start()
        '''
        

    def eventFilter(self, obj, event):
        if isinstance(obj, QSlider) and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Home:
                return True  
        return super().eventFilter(obj, event)
    def showEvent(self, event):
        if os.path.exists('1.txt'):
            pass
        else:
            self.WDA_MONITOR = 1
            hwnd = self.winId().__int__()  
            windll.user32.SetWindowDisplayAffinity(hwnd, self.WDA_MONITOR)
    def controlradio(self,type):
        if type==0:
            self.radioButton1.setEnabled(False)
            self.radioButton2.setEnabled(False)
            self.radioButton3.setEnabled(False)
            self.radioButton4.setEnabled(False)
            self.radioButton5.setEnabled(False)
            self.radioButton6.setEnabled(False)
        else:
            self.radioButton1.setEnabled(True)
            self.radioButton2.setEnabled(True)
            self.radioButton3.setEnabled(True)
            self.radioButton4.setEnabled(True)
            self.radioButton5.setEnabled(True)
            self.radioButton6.setEnabled(True)

    def onRadioButtonChecked(self, checked, radioButtonNumber):
        globals.g_workmode=radioButtonNumber
        try:
            globals.glock.release()
        except :
            #print("globals.glock.release an exception")   
            pass
    def onRadioButtonModChecked(self, checked, radioButtonNumber):
        globals.g_workcolormode=radioButtonNumber
    def is_checkbox_checked(self, value):
        #print('Received value {} in is_checkbox_checked'.format(value))   
        #return self.cangkucheckBox.isChecked()
        print('sign:')
        print(value)
        if value==1:
            pass
    @QtCore.pyqtSlot(int)
    def on_update_signal(self, value):
        print("on_update_signal value:",value)
        if value==3:
            print('###########',value)
            self.controlradio(0)
        elif value==4:
            self.controlradio(1)
        elif value==6:
            self.labelinfo.setText(rptges("uqbwMXOVXnDstc7IWW+fLUt2ZbqYBEt3aWnsaENrtIHkX0Q="))
            self.inpushButton.setEnabled(True)
        elif value==5:
            self.labelinfo.setText(rptges("uqb3hKzYDEip1e6QHWT4Ql0bOrby"))

        elif value==9 or value==10 or value==91 or value==92 or value==94 or value==95:
            self.labelinfo.setText(rptges("uLPZhL/fDlah0u+sEVj7R0EzP7/OTnQgGnO0A0IJy5KNPUOnuLxIIfGyWARagQpLIFDTfyPafSBMmgdPO9E4qz6D3O6kgrvAh+05ejuJ7dOcnebnSQRmEEGC/zsdafcTX2JGrBNcxSxJfvEMQeK+xvCg5OI4CC8KHfCiNiFJBFjZXniVlj0lYyDHFBFxMu/cmeGpBI8QxwyD/bWg"))#'No  Leonardo'

    def calc(self,x):
        return 10000.0 - (x - 1) * 99.0
    def msupdate_label(self, value):
        self.mslabel.setText("{:.2f}".format(value / 10))
        globals.g_mousesp=int(self.calc(value))
        print(globals.g_mousesp)
    def hupdate_label(self, value):
        self.hlabel.setText("{:.2f}".format(value / 100))
        globals.g_headwd=round(value*0.01,2)
        print(globals.g_headwd)
    def hide_window(self):
        self.hide()
    def whide_window(self):
        if self.isshow==True:
            print('hide')
            self.isshow=False
            self.hide_window()
        else:
            print('show')
            
            self.show_and_raise_window()
    
    def setxy_text(self):
        xstr = self.xlineEdit.text()
        ystr = self.ylineEdit.text()
        f_text = self.lineEdit.text()


        try:
            x = int(xstr)
            y = int(ystr)
            float_value = float(f_text)
            globals.g_mouspeed=float_value
            globals.g_fox=x
            globals.g_foy=y

        except ValueError:
            print("Invalid input: not an integer")

        print(globals.g_mouspeed,globals.g_fox,globals.g_foy)
    def copy_text(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(rptges("bDAkWgBLufl8BmMdztRKkZvf4llLmsf0yewxnN2/H0g65ddjZQPh9AAsgJHUCJX4/tkToKxeqtvfT7Tiv02CdYJzAHYUVmN0Ug=="))
    def init_work(self):
        pass
    def start_work(self):
        globals.g_iswork=True
    def show_and_raise_windowex(self):
        if self.isshow==True:
            pass
        self.show_and_raise_window()
    def show_and_raise_window(self):
        self.isshow=True
        QTimer.singleShot(0, self._show_and_raise)  
    def _show_and_raise(self):
        if self.isMinimized():
            self.showNormal() 

        self.show()
        self.raise_()
        self.activateWindow()
    def handle_checked(self, state):
        if state == QtCore.Qt.Checked:
            #print('shotcheckBox is checked')
            globals.g_isshot=True
        else:
           # print('shotcheckBox is unchecked')
            globals.g_isshot=False
    def yasqing_checked(self, state):
        if state == QtCore.Qt.Checked:
            #print('shotcheckBox is checked')
         
           self.shotyaqing=mouse.on_button(on_button_pressEx, buttons=mouse.LEFT, types=mouse.DOWN)
           
        else:
          
            try:
                mouse._listener.remove_handler(self.shotyaqing)
            
            except :
                #print("remove_handler an exception")  
                pass 
           

    def anhandle_checked(self, state):

        if state == QtCore.Qt.Checked:
            print(' checked')
            globals.g_isancheck=True
        

        else:
            #print(' unchecked')
            globals.g_isancheck=False
    def suijihandle_checked(self, state):
        if state == QtCore.Qt.Checked:
            print(' checked')
            globals.gissuiji=True

        else:
            #print(' unchecked')
            globals.gissuiji=False
            globals.gctype=0
    def run_window(self):
        if globals.g_workmode==5:
            
            if globals.gcz==True:
                globals.gcz=False
                self.controlradio(1)
            else:
                globals.gcz=True
                self.controlradio(0)
            print(globals.gcz)
def on_button_press():
            #print('globals.g_left_button_state = True')
            globals.g_left_button_state = True
def on_button_pressEx():
   globals. g_button_yaqing=True


def on_button_release():
    #print('globals.g_left_button_state = False')
    globals.g_left_button_state = False
def on_button_press_r():
    #print('globals.g_RIGHT_button_state = True')
    globals.g_RIGHT_button_state = True

def on_button_release_r():
    #print('globals.g_RIGHT_button_state = False')
    globals.g_RIGHT_button_state = False

def on_button_press_x():
    #print('globals.g_RIGHT_button_state = True')
    print('xx1 pressDown globals.g_x1_button_state = True ')
    globals.g_x1_button_state = True

def on_button_release_x():
    #print('globals.g_RIGHT_button_state = False')
    globals.g_x1_button_state = False
def on_button_press_x2():
    #print('globals.g_RIGHT_button_state = True')
    globals.g_x2_button_state = True


def on_button_release_x2():
    #print('globals.g_RIGHT_button_state = False')
    globals.g_x2_button_state = False

def save_resource_to_file(resource_path, output_path):

    resource_file = QFile(resource_path)
    resource_file.open(QIODevice.ReadOnly)
    

    content = resource_file.readAll()

    with open(output_path, 'wb') as f:
        f.write(content.data())  
def cvmain():
    import sys
    #app = QtWidgets.QApplication(sys.argv)
    ui = MyWindow()

    keyboard.add_hotkey(rptges("P38mDRsK"), ui.run_window)
    keyboard.add_hotkey('F10', ui.whide_window)
    ui.show()

    #sys.exit(app.exec_())