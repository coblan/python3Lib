from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import  *

import pickle, re
from heQt.tabWidget_p.barBase import BarBase
from heStruct.cls import sub_obj_call, add_sub_obj

class TabWidgetBase(QTabWidget):
    """
    默认向QTabWidget增加的功能：
    1 迭代窗口
    2 保存，恢复所有能够pickle的窗口
    
    可以开启功能：
    1 enableCrossDrag   自定义的拖动。可以垮Tabwidget拖动
    2 enableChineseDirection  中文旋转 。利用自绘中文来实现。
                              如果还需要拖动，最好开启"1 自定义拖动"，因为Qt自带拖动，自绘标签有空白。
    
    """
    def __init__(self, *args):
        super().__init__( *args)

        self.tabCloseRequested.connect(self.removeTab)

    def enableCrossDrag(self, cusBar = BarBase):
        """注意：cusBar是BarBase<-Bar的子类，**不是** 类对象"""
        if not hasattr(self, "cusBar"):
            self.cusBar = cusBar(self)
            self.setTabBar(self.cusBar)
        self.cusBar.enableCrossDrag()
        self.crossDrag = _crossDrag(self, self.cusBar.comDrag)
        add_sub_obj(self, self.crossDrag)

    def enableChineseDirection(self, cusBar = BarBase):
        if not hasattr(self, "cusBar"):
            self.cusBar = cusBar(self)
            self.setTabBar(self.cusBar) 
        self.cusBar.enableChineseDirection()
    @sub_obj_call
    def dragEnterEvent(self, event):
        pass
    @sub_obj_call
    def dropEvent(self, event):
        pass 
    @sub_obj_call
    def dragMoveEvent(self, event):
        super().dragMoveEvent(event)
    @sub_obj_call
    def dragLeaveEvent(self, event):
        pass   
    #[1] 迭代窗口
    def __iter__(self):
        self.iterIndex=-1
        return self    
    def __next__(self):
        self.iterIndex += 1
        if self.iterIndex < self.count():
            return self.widget( self.iterIndex )
        raise StopIteration    
    
    #[2] 添加窗口，添加标签名，将名字标签名保存在windowTitle中
    def addTab(self, widget, name_icon = "", name = ""):
        widget.tabWidget_ = self
        if isinstance(name_icon, QIcon):
            widget.setWindowTitle(name)
            if self.isNeedTurnDirection(name):
                return super().addTab(widget, name_icon)
            else:
                return super().addTab(widget, name_icon, name)
        else:
            widget.setWindowTitle(name_icon)
            if self.isNeedTurnDirection(name_icon):
                return super().addTab(widget, "")
            else:
                return super().addTab(widget, name_icon)
    
    def insertTab(self, index, widget, name_icon , name = None):
        widget.tabWidget_ = self
        if isinstance(name_icon, QIcon):
            widget.setWindowTitle(name)
            if self.isNeedTurnDirection(name):
                super().insertTab(index, widget, name_icon)
            else:
                super().insertTab(index, widget, name_icon, name)
        else:
            widget.setWindowTitle(name_icon)
            if self.isNeedTurnDirection(name_icon):
                super().insertTab(index, widget, "")
            else:
                super().insertTab(index, widget, name_icon)    
                
    def removeWidget(self, widget):
        index = self.indexOf(widget)
        if index >= 0:
            self.removeTab(index)
       
    #[3] 保存和恢复所有的窗口。保存数据是QByteArray形式，便于同qt对接
    def restoreWins(self, string):
        if not string:
            return
        if isinstance(string, QByteArray):
            string = string.data()
        dc = pickle.loads(string)
        ls = dc.get('wins', None)
        if ls:
            last = None
            currentWidget = None
            for ii in ls:
                if ii == "last is currentWidget":
                    currentWidget = last
                    continue
                else:
                    # 恢复窗口及其tabName属性
                    win, label, tip = pickle.loads(ii[0]), ii[1], ii[2]
                    index = self.addTab(win, label)
                    self.setTabToolTip(index, tip)
                    last = win
            if currentWidget:
                self.setCurrentWidget(currentWidget )
          

    def saveWins(self):
        ls = []
        index = -1
        for win in self:
            index += 1
            try:
                winbyt = pickle.dumps(win)
                # 保存窗口及其tabName属性
                label = win.windowTitle()
                tip = self.tabToolTip(index)
                ls.append( (winbyt, label, tip) )
                if self.currentWidget() == win:
                    ls.append("last is currentWidget")          
            except Exception as e:
                print(e)
            
            
        byte = pickle.dumps( {'wins': ls } )
        return QByteArray(byte)

    def isNeedTurnDirection(self, text):
        """sub_obj .hook 函数"""
        return False

    def setTabPosition(self, pos):
        super().setTabPosition( pos)
        index = -1
        for win in self:
            index += 1
            title = win.windowTitle()
            if self.isNeedTurnDirection(title):
                self.setTabText(index, "")    
        

class _crossDrag:
    """与bar的_crossDrag组件一起构成了Tabwidget的拖拽功能"""
    def __init__(self, tabwidget, bar_comdrag):
        self.tabwidget = tabwidget
        tabwidget.setAcceptDrops(True)
        self.bar_comdrag = bar_comdrag
        
    def dragEnterEvent(self, event):
        event.acceptProposedAction()
    def dropEvent(self, event):
        mime = event.mimeData()
        self.tabwidget.addTab(mime.win, mime.win.windowTitle() ) 
        self.bar_comdrag.line = None
        self.tabwidget.tabBar().update()   
        
    def dragMoveEvent(self, event):
        self.bar_comdrag.drawLine( -1)
    def dragLeaveEvent(self, event):
        self.bar_comdrag.line = None
        self.tabwidget.tabBar().update()     