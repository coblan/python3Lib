import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from uploadWin import UploadWin
from loginWin import LoginWin
from interface import get_data,upload,get_list

def show_mainwin(login_return):
    if login_return:
        win = UploadWin(get_metalist=get_list, get_metainfo=get_data,upload_metainfo=upload)
        win.show()
        sys.dog = win

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = LoginWin()
    login.show()
    login.login_ok.connect(show_mainwin)
    sys.exit(app.exec_())