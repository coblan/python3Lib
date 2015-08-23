from heQt.dockWidget_p.dockWidgetBase import DockWidgetBase
from heQt.dockWidget_p.dockPanelBase import DockPanelBase
from heOs.pickle_ import IPickle
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
class DockWidget(DockWidgetBase):
    """
    dock类，具有左中右三个位置，用于放置面板。注意面板必须是DockTab的子类。这些面板可以随意拖拽。
    例子:
    mainWin=QMainWindow()
    mainWin.dock=DockWidget()
    mainWin.setCentralWidget(mainWin.dock)
    
    mainWin.dock.setCentralWidget( QWidget() )  # 你自己的QWidget
    
    # 添加标签页，位置可以是左中右三种
    mainWin.panel1=DockPanel()
    mainWin.dock.addLeft( mainWin.panel1)
    mainWin.panel1.addTab(win)
    
    1. 注意 addLeft(tabWin),addMiddle(tabWin),addRight(tabWin)添加tabWin,这个tabWin必须是DockPanel的对象。
       因为其实现了拖拉等动作
    2. 只能保存那些能够pickle的窗口,所以如果想要保存panel状态，需要实现pickle功能
    
    """    
    pass

class DockPanel(DockPanelBase):
    """放在DockWidget中的标签页的容器"""
    pass

############################
#  测试代码
#############################
class Lab(IPickle, QLabel):
    def __init__(self, *args):
        super().__init__( *args)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.addAction(QAction("fff", self))
    def install(self, tab):
        tab.addTab(self, "haha")
    def __reduce__(self):
        self.pickleDict = {"text": self.text()}
        return super().__reduce__()
    def __setstate__(self, state):
        self.setText(state.get("text", None))
        
def test():
    tt, ok = QInputDialog.getText(None, "s", "f")
    if not ok:
        return
    tab = DockPanel ()
    
    tab.addTab(Lab("middle"), "当前目录")
    tab.addTab(Lab("middle"), "大纲")
    tab.addTab(QWidget(), "can't save ")
    getattr(win, tt)(tab)
    
if __name__ == "__main__":

    import sys
    from heQt.mainWidget import MainWidget
    app = QApplication(sys.argv)
    mainWin = MainWidget()
    mainWin.enableSaveSession()
    
    win = DockWidget()
    mainWin.setCentralWidget(win)
    mainWin.show()
    
    btn = QPushButton("cli")
    btn.clicked.connect(test)
    btn.show()
    
    #tab = DockTab()
    #tab.addTab(QWidget(), "hhh")
    #tab.addTab(QWidget(), "jjhh")
    #win.addLeft(tab)
    
    #tab2 = DockTab()
    #tab2.addTab(QWidget(), "hhh")
    #tab2.addTab(QWidget(), "jjhh")    
    
    #win.addMiddle(tab2)
    
    mainWin.registeSaveItem(win.restoreDock, win.saveDock, "dock")
    
    mainWin.restoreAll()
    sys.exit(app.exec_())