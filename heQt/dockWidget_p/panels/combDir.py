from qt_.qtEven import * 
from struct_.pickleInterface import IPickle
from qt_.view_.modelView_.itemView import TreeView
#from qt_.view_.dock_.tabWin import TabItem
from qt_.view_.stdoutView import StdoutView
from qt_.widget.dockWidget_.panels.uis.combDirView_ui import Ui_Form
#from qt_.widget.dockWidget import DockPanel
import os.path
import  sys

from struct_.objs import walk_objTree
from .base import Base


class CombDir(Base, QWidget, Ui_Form):
    """当前目录视图
    sys.state:
             openFunc :
    """
    def __init__(self):
        # 注意不要传参数，因为要pickle不了参数
        super().__init__( )
        self.setupUi(self)

        self.setWindowTitle("当前目录")
        self.dirView.addDirOp()
        self.dirView.setHeaderHidden(True)
        self.dirView.doubleClicked.connect(self.DBOpenCodeFile)
         
        self.dbOpenFilter = None
        
        self.plus.clicked.connect(self.addDir)
        self.minus.clicked.connect(self.rmDir)
        self.comb.currentIndexChanged[str].connect(self.on_combChanged)
        
        # 打开函数，实例化的时候设置。例如mainWidget的opencode函数
        self.openFunc = None
        
    def addDir(self):
        dir_= QFileDialog.getExistingDirectory()
        if dir_:
            self.comb.addItem(dir_)
            index = self.comb.count() - 1
            self.comb.setCurrentIndex(index)
            self.comb.setItemData(index, dir_, Qt.ToolTipRole)
    def rmDir(self):
        self.comb.removeItem(self.comb.currentIndex())
    def on_combChanged(self, ustr):
        self.dirView.setRootEx(ustr)
        
    def initState(self):
        self.openFunc = sys.state["openFunc"]
        super().initState()
        

        
    def __reduce__(self):
        c = self.comb.count()
        wds = []
        for i in range(c):
            wds.append((self.comb.itemText(i), self.comb.itemData(i, Qt.ToolTipRole)) )
        self.pickleDict["item"] = wds
        self.pickleDict["current_index"] = self.comb.currentIndex()
        self.pickleDict["object_name"] = self.objectName()
        return super().__reduce__()
  
    def __setstate__(self, state):
        wds = state["item"]
        index = state["current_index"]
        now = -1
        for text, tip in wds:
            self.comb.addItem(text)
            now += 1
            self.comb.setItemData(now, tip, Qt.ToolTipRole)
        self.comb.setCurrentIndex( index )  
        self.dirView.setRootEx(self.comb.currentText())
        self.setObjectName(state["object_name"])

    def DBOpenCodeFile(self, idx):
        cplt_nm= self.dirView.filePathFromIndex(idx)
        self.openFunc(cplt_nm)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CombDirPanel()
    win.show()
    sys.exit(app.exec_())