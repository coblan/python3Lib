from PyQt5.QtWidgets import *

from heQt.tabWidget_p.barBase import BarBase
from heQt.tabWidget_p.tabWidgetBase import TabWidgetBase
import pickle, re
class TabWidget(TabWidgetBase):
    """
    默认增加功能：
    1 迭代窗口
    2 保存，恢复所有能够pickle的窗口
    
    重要函数：
    enableCrossDrag(Bar<-cls)           开启夸窗口拖拽功能
    enableChineseDirection(Bar<-cls)    开启中文调整方向功能
    
    注意：这两个函数的参数是Bar的子类，不是Bar的对象
    """
    pass
class Bar(BarBase):
    """
    用在TabWidget.enableCrossDrag的参数中
    因为跨窗口拖动和调整中文方向，都需要更改QTableWidget.tabbar对象的行为，所以自定义了这个Bar，在enableXXX中会自动替换原tabbar。
    可以被继承实现更多功能
    """
    pass
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    man = QMainWindow()
    win = TabWidget()
    #bar = Bar(win)
    #win.setTabBar(bar)
    win.enableCrossDrag()
    win.enableChineseDirection()
    #win.setMovable(True)
    man.setCentralWidget(win)
    man.show()    
    win.addTab(QTextEdit(), "haha")
    win.addTab(QTextEdit(), "中文")
    win.addTab(QTextEdit(), "英文")
    win.setTabPosition(QTabWidget.West)
    win.setTabsClosable(True)
    
    win2 = TabWidget()
    
    #bar2 = Bar(win2)
    #win2.setTabBar(bar2)
    win2.enableCrossDrag()
    win2.enableChineseDirection()
    win2.show()
    win2.setTabsClosable(True)
    #win2.addTab(QTextEdit(), "jjj")
    sys.exit(app.exec_())