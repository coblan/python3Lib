#! encoding=utf8
import sys,os

sys.path.append("python")
os.environ["path"] += ";dlls"

from heQt.qteven import *
from uploadWin import UploadWin
from loginWin import LoginWin
from interface import get_data,upload,get_list

#dlls = os.path.join(os.getcwd(),'dlls')
#sys.path.append(dlls)


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