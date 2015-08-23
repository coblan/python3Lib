from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from heStruct.cls import sub_obj_call, add_sub_obj
import re
class BarBase(QTabBar):
    """用在TabWidgetBase中，用来增加功能，比如调整中文方向，垮窗口拖动标签"""
    def __init__(self, p , *args):
        super(BarBase,self).__init__(p, *args)
        self.tabwidget = p
        self.tabHigh = 20

    def enableChineseDirection(self):
        self.comChinese = _ChineseDirection(self)
        add_sub_obj(self, self.comChinese)
    
    def enableCrossDrag(self):
        self.comDrag = _crossDrag(self)
        self.comDrag.install()
       
 
    @sub_obj_call
    def mouseMoveEvent(self, event):
        super(BarBase,self).mouseMoveEvent(event)
    @sub_obj_call
    def mousePressEvent(self, event):
        super(BarBase,self).mousePressEvent(event)
    @sub_obj_call      
    def dragMoveEvent(self, event):
        super(BarBase,self).dragMoveEvent(event)
    @sub_obj_call
    def dragEnterEvent(self, event):
        pass
    @sub_obj_call
    def dragLeaveEvent(self, event): 
        pass
    @sub_obj_call
    def dropEvent(self, event):
        pass
    @sub_obj_call
    def paintEvent(self, event):
        super(BarBase,self).paintEvent(event)
        
        
class _ChineseDirection(QObject):
    """能够调整中文的方向"""
    def __init__(self, bar):
        super().__init__(bar)
        self.tabwidget = bar.tabwidget
        self.bar = bar
        self.tabwidget.isNeedTurnDirection = self.isNeedTurnDirection
        self.old_bar_tabSizeHint = self.bar.tabSizeHint
        self.bar.tabSizeHint = self.tabSizeHint
        
    def isNeedTurnDirection(self, text):
        if self.tabwidget.tabPosition() != QTabWidget.North:
            if not re.match("^[A-Za-z]", text):
                return True
        return False   
    def tabSizeHint(self, index):
        win = self.tabwidget.widget(index)
        if not self.isNeedTurnDirection(win.windowTitle()):
            return self.old_bar_tabSizeHint(index)  

        size = QSize()
        size.setHeight(self.bar.fontMetrics().height() * len(win.windowTitle()))
        size.setWidth(20)
        size.setHeight(size.height() + 20)
        return size
    
    def paintEvent(self, event):
        painter = QPainter(self.bar)

        # 单独画中文
        for win in self.tabwidget:
            tooltip = win.windowTitle()
            if self.isNeedTurnDirection(tooltip):
                rect = self.bar.tabRect(self.tabwidget.indexOf(win))
                rect.translate(3, 8)
                painter.drawText(rect, Qt.TextWordWrap , tooltip)          

class _crossDrag:
    """实现自定义的垮tabwidget的拖动。其还需要tabwidget中的_crossDrag的配合"""
    def __init__(self, bar):
        self.bar = bar
        self.tabwidget = bar.tabwidget
    def install(self):
        self.bar.setAcceptDrops(True)
        self.line = None
        add_sub_obj(self.bar, self)
        
    def dragMoveEvent(self, event):
        tabIdx = self.bar.tabAt( event.pos())
        self.drawLine(tabIdx)
        
    def drawLine(self, tabIdx):
        if tabIdx == -1:
            tabIdx = self.bar.count() - 1
            rect = self.bar.tabRect(tabIdx)
            if self.tabwidget.tabPosition() == QTabWidget.North:
                self.line = ( rect.topRight(), rect.bottomRight() )
            else:   
                self.line = ( rect.bottomLeft(), rect.bottomRight() )            
        else:
            
            rect = self.bar.tabRect(tabIdx)
            if self.tabwidget.tabPosition() ==  QTabWidget.North:
                self.line = ( rect.topLeft(), rect.bottomLeft() )
            else:   
                self.line = ( rect.topLeft(), rect.topRight() )
        self.bar.update()
    def dragEnterEvent(self, event):
        event.acceptProposedAction()
    def dragLeaveEvent(self, event):
        self.line = None
        self.bar.update()
    def dropEvent(self, event):
        mime = event.mimeData()
        tabIdx = self.bar.tabAt( event.pos())
        if tabIdx != -1:
            self.tabwidget.insertTab(tabIdx, mime.win, mime.win.windowTitle())
        else:
            self.tabwidget.addTab(mime.win, mime.win.windowTitle())
        
        self.line = None
        self.bar.update()
    def paintEvent(self, event):
        painter = QPainter(self.bar)
        # 画拖动时的线条
        if self.line:
            pen = QPen()
            pen.setColor(Qt.red)
            pen.setWidth(3)
            painter.setPen(pen)
            painter.drawLine(self.line[0], self.line[1])    
    def mousePressEvent(self, event):
        self.bar.pressPos = event.pos()
    def mouseMoveEvent(self, event):
        self = self.bar
        if not (event.buttons() & Qt.LeftButton):
            return
        if ((event.pos() - self.pressPos).manhattanLength() < QApplication.startDragDistance()):
            return      

        itemIdx = self.tabAt(self.pressPos)
        if itemIdx == -1:
            return
        
        drag = QDrag(self)
        mimeData = QMimeData()
        mimeData.win= self.tabwidget.widget(itemIdx)
        drag.setMimeData(mimeData)
   
        dropAction = drag.exec_(Qt.CopyAction | Qt.MoveAction) 