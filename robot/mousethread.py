import mouse
from PyQt5.QtCore import QThread, pyqtSignal,QTime
import globals 
import time
class MouseWorker(QThread):
    check_status = pyqtSignal()
    update_signal = pyqtSignal(int)

    def __init__(self, callback, parent=None):
        super().__init__(parent)
        self.check_callback = callback

    def is_DN_key_pressed(self,type):
            #阻塞的
        print('is_DN_key_pressed #############',type)
        if type==1:
            mouse.wait(button=globals.X, target_types=(globals.DOWN))
        if type==2:
            mouse.wait(button=globals.X2, target_types=(globals.DOWN))
    def run(self):
        print('#############33')
        while True:
            if globals.g_iswork==False:
                time.sleep(1)
                continue
            if globals.g_workmode==3 :
                if self.is_DN_key_pressed(1):
                    if globals.gm4==False:
                        globals.gm4=True
                        print('tttt\n')
                        self.update_signal.emit(3)
                    else:
                        globals.gm4=False
                        self.update_signal.emit(4)
            elif globals.g_workmode==4 :
                if self.is_DN_key_pressed(2):
                    if globals.gm5==False:
                        
                        globals.gm5=True
                        self.update_signal.emit(3)
                    else:
                        globals.gm5=False
                        self.update_signal.emit(4)
            time.sleep(1)


       