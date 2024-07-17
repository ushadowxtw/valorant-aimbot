from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from datetime import datetime
import hashlib
import mainwindow_ui
import check 
import cvmain
import subprocess


class MyWindow(QtWidgets.QMainWindow, mainwindow_ui.Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.on_button_clicked)

    def is_valid_str(self,s):
        if len(s) == 12 and s.isalnum():
            return True
        return False
    @QtCore.pyqtSlot()
    def on_button_clicked(self):
        text = self.filenamelineEdit.text()
        ret=True
        print(text)
       # if self.is_valid_str(text)==True:
            #check
           # ret=check.checkauth(text)
        if ret==True:
            self.hide()
            cvmain.cvmain()
            return

        mstr=self.calculate_md5(text)
        self.label.setText(mstr)
    def calculate_md5(self,string):
        md5 = hashlib.md5()
        md5.update(string.encode('utf-8'))
        return md5.hexdigest()
    def show_popup(self, title, text):
        QMessageBox.information(self, title, text)
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