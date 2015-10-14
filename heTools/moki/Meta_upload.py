import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWebKitWidgets import *
from PyQt5.QtCore import *


class Browser(QWebView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.page().setLinkDelegationPolicy( QWebPage.DelegateAllLinks )
        self.linkClicked.connect(self.on_link)
    
    def on_link(self,url):
        self.load(url)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Browser()
    win.load( QUrl('http://ps.stm.com/admin/metadata/metadatainfo/?p=2') )
    #win.load(QUrl('http://www.163.com'))
    win.show()
    sys.exit(app.exec_())