import keyboard
from PyQt5.QtCore import QThread, pyqtSignal,QTime
import globals 
import globals  # 导入包含全局变量的模块
class KeyBoardWorker(QThread):
    check_status = pyqtSignal()
    update_signal = pyqtSignal(int)

    def __init__(self, callback, parent=None):
        super().__init__(parent)
        self.check_callback = callback
    def run(self):
        #return
        while True:
            event = keyboard.read_event()
            if globals.g_workmode==6:#ctrl模式
                if event.name == 'ctrl' and event.event_type == keyboard.KEY_DOWN :
                    globals.g_ctrlisdown=True
                elif event.name == 'ctrl' and event.event_type == keyboard.KEY_UP :
                    globals.g_ctrlisdown=False
                    globals.g_ctrliswork=False
                else:
                    pass
            else:
                pass