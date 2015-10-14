from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from login_ui import Ui_Form
from interface import login
import sys

class LoginWin(QWidget,Ui_Form):
    login_ok = pyqtSignal(object)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('MetaInfo upload tool login')
        
        self.btn_login.clicked.connect(self.on_login)
        self.btn_quit.clicked.connect(self.on_quit)
        
    def on_login(self):
        name = self.account.text()
        psw = self.passtext.text()
        
        rt = login(name,psw)
        if rt:
            self.login_ok.emit(rt)
            self.hide()
    
    def on_quit(self):
        sys.exit(0)