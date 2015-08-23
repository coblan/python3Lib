from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from heQt.tabWidget import TabWidget, Bar

import re
from heOs.pickle_ import IPickle
class DockPanelBase(IPickle, TabWidget):
    """
    开启了TabWidget的中文调整方向，自定义拖拽功能
    增加了点击标签切换开关。该功能主要在TabWidget.Bar<- customBar类中实现。
    
    """
    postion = [QTabWidget.North, QTabWidget.South, QTabWidget.East, QTabWidget.West]
    def __init__(self, *args):
        super().__init__( *args)
        #self.setTabBar(Bar(self))
        self.setMinimumWidth(20)
        self.setMinimumHeight(20)
        self.setAcceptDrops(True)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        
        act = QAction("移除本面板", self)
        self.addAction(act)
        act.triggered.connect(self.uninstall)
        
        self.enableCrossDrag(customBar)
        self.enableChineseDirection(customBar)
    def uninstall(self):
        ls = []
        for win in self:
            ls.append(win)
        for win in ls:
            if hasattr(win, "uninstall"):
                win.uninstall()
        #print(self.parentWidget())
        p = self.parentWidget()
        self.setParent(None)
        if not p.count():
            p.setParent(None)
            p.added = False
            #pp = p.parentWidget()
            #if not isinstance(pp, QSplitter):
                #return
            #sizes = pp.sizes()
            #if self.tabPosition() == self.East:
                #pp.setSizes([0, sizes[0] + sizes[1], sizes[2]])
            #elif self.tabPosition() == self.West:
                #pp.setSizes([sizes[0], sizes[1] + sizes[2], 0])
            #elif self.TabPosition() == QTabWidget.North:
                #self.grandParSplitter.setSizes( [sizes[0] + sizes[1], 0 ])
                
    def install(self, splitter, outterSplit, pos):
        self.splitter = splitter
        self.tabBar().mainSplit = outterSplit
        self.tabBar().tabWidget = self
        
        self.grandParSplitter = outterSplit
        if splitter.orientation() == Qt.Vertical:
            #ls = [QTabWidget.East, QTabWidget.North, QTabWidget.West]
            #self.setTabPosition(ls[index])
            self.setTabPosition(pos)
            
        #self.tabBar().index = index
        self.tabBar().outSplit = splitter
        
        splitter.addWidget(self)
   
    # pickle 支持
    def __reduce__(self):
        self.pickleDict = {"wins": self.saveWins(), 
                           "position": self.postion.index(self.tabPosition()), 
                           "objectName": self.objectName(),}

        return super().__reduce__()
    def __setstate__(self, state):
        self.setObjectName(state["objectName"])
        wins = state.get("wins", None)
        self.setTabPosition(self.postion[ state.get("position", 0) ])
        if wins:
            self.restoreWins(wins)
        
    
class customBar(Bar):
    """增加点击激活标签，隐藏相应的面板  的功能"""
    #def __init__(self,  *args):
        #super().__init__( *args)
        #self.clickOnActive = False

    def contextMenuEvent(self, event):
        pos = event.globalPos ()
        menu = QMenu()
        win = self.tabwidget.widget( self.tabAt(event.pos () ) )
        if hasattr(win, "barActions"):
            menu.addActions(win.barActions)
        menu.addActions(self.tabwidget.actions())
        menu.exec_(pos)
    #def mouseDoubleClickEvent(self, e):
        #super().mouseDoubleClickEvent(e)
        #wid = self.mainSplit.sizes()
        ##if self.orient == 0:
        ##print(wid[self.index])
        #if wid[self.index] <= self.tabHigh:
            #wid[self.index] = self.tabwidget.parentWidget().openedWidth
        #else:
            #self.tabwidget.parentWidget().openedWidth = wid[self.index]
            ##self.tabwidget.parentWidget().openWid = self.openWid
            #wid[self.index] = self.tabHigh
        #self.mainSplit.setSizes(wid)
    
    def switchPanel(self):
        wid = self.mainSplit.sizes()
        index = self.mainSplit.indexOf(self.outSplit)
        if index == 0:
            absorb_index = 1
        elif index == 1:
            absorb_index = 0
        elif index == 2:
            absorb_index = 1
            
        if wid[index] <= self.tabHigh:
            #wid[index] = self.tabwidget.parentWidget().openedWidth
            wid[index] = self.outSplit.openedWidth
            wid[absorb_index] -= (self.outSplit.openedWidth - self.tabHigh)
        else:
            #self.tabwidget.parentWidget().openedWidth = wid[index]
            self.outSplit.openedWidth = wid[index]
            wid[absorb_index] += ( wid[index] - self.tabHigh)
            wid[index] = self.tabHigh
            
        self.mainSplit.setSizes(wid) 
    def mousePressEvent(self, event):
        pos = event.pos()
        self.shouldSwitch = False
        if self.currentIndex() == self.tabAt(pos) and event.button() == Qt.LeftButton :             
            self.shouldSwitch = True                          # self.shouldSwitch 的存在是因为切换标签是在mousePressEvent完成
        super().mousePressEvent(event)                         # "开关面板"，是在mouseReleaseEvent中完成，所以必须在mousePressEvent
        self.pressed = True                                    # 中记录下是否应该"开关面板"。
    def mouseReleaseEvent(self, event):
        if self.shouldSwitch :
            self.switchPanel()
        else:
            super().mouseReleaseEvent(event)


    #def mouseMoveEvent(self, event):
        #self.clickOnActive = False
        #super().mouseMoveEvent(event)
    
    #def switchPanel(self):
        #hight = QWidget.height(self.tabwidget)
        #split = self.mainSplit
        
        #self.tabwidget.resize(20, hight)
        

