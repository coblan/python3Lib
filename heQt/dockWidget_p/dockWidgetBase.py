from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import pickle
class DockWidgetBase(QSplitter):
    """
    dock类，具有左中右三个位置，用于放置面板。注意面板必须是DockTab的子类。这些面板可以随意拖拽。
    例子:
    mainWin=QMainWindow()
    mainWin.dock=Dock().install(mainWin)
    
    mainWin.dock.setCenterWidget( QWidget() )  # 你自己的QWidget
    
    # 添加标签页，位置可以是左中右三种
    mainWin.tab1=DockPanel()
    mainWin.addLeft( mainWin.tab1)
    mainWin.tab1.addTab(win,win.name)
    
    1. 注意 addLeft(tabWin),addMiddle(tabWin),addRight(tabWin)添加tabWin,这个tabWin必须是DockPanel的对象。
    2. mainWin.tab1.addWin(win) 的 win必须要有install函数,且能够pickle,参见 Lab类定义 .或者: tabWin.TabItem
    
    """    
    def __init__(self, *args):
        super().__init__( *args)
        self.left = QSplitter(Qt.Vertical)
        self.middle = QSplitter(Qt.Vertical)
        self.right = QSplitter(Qt.Vertical)   
        
        
        self.left.added = False
        #self.addWidget(self.left)
        self.addWidget(self.middle)
        self.right.added = False
        #self.addWidget(self.right)        
        
        self.middle.addWidget(QLabel("middle"))
        self.middle.split = QSplitter()
        #self.middle.setStretchFactor(0, 1)
        #self.middle.setStretchFactor(1, 0)
        self.middle.split.added = False
        #self.middle.addWidget(self.middle.split)  
        
        #self.setStretchFactor(0, 0)
        #self.setStretchFactor(1, 1)
        #self.setStretchFactor(2, 0)        
        
        self.setChildrenCollapsible(False)
                
        self.left.openedWidth = 30
        self.right.openedWidth = 30
        self.middle.split.openedWidth = 30         
        
        self.left.p_spit = self
        self.right.p_spit = self
        self.middle.split.p_spit = self.middle
    
    #def updateStretchFactor(self):
        #if self.
        #self.setStretchFactor(0, 0)
        #self.setStretchFactor(1, 1)
        #self.setStretchFactor(2, 0)           
    def addLeft(self, tabWin):
        if not self.left.added:
            self.insertWidget(0, self.left)
            self.left.added = True
            
        tabWin.install(self.left, self, QTabWidget.East)
        return tabWin
        
    def addRight(self,  tabWin):
        if not self.right.added:
            self.addWidget( self.right)
            self.right.added = True        
        tabWin.install(self.right, self, QTabWidget.West)
        return tabWin
    def addMiddle(self, tabWin):
        if not self.middle.split.added:
            self.middle.addWidget( self.middle.split)
            self.middle.split.added = True 
            self.middle.setStretchFactor(0, 1)
            self.middle.setStretchFactor(1, 0) 
            
        tabWin.install(self.middle.split, self.middle, QTabWidget.North)
        return tabWin
    def setCentralWidget(self, win):
        self.middle.widget(0).setParent(None)
        self.middle.insertWidget(0, win)
        self.middle.setStretchFactor(0, 1)
        self.middle.setStretchFactor(1, 0)

    def saveDock(self):
        state = {}
        state["state"] = self.saveState()
        state["left"] = self._saveSplit(self.left)
        state["middle"] = self._saveMiddle()
        state["right"] = self._saveSplit(self.right)
        return QByteArray( pickle.dumps(state))
    def restoreDock(self, QByt):
        if not QByt:
            return
        if isinstance(QByt, QByteArray):
            QByt = QByt.data()
        state = pickle.loads(QByt)
        self._restoreSplit(state, self.addLeft, "left")
        self._restoreSplit(state, self.addRight, "right")
        self._restoreMiddle(state)
        
        self.restoreState(state.get("state", None))   
        
    def _saveSplit(self, split):
        dc = {"state" : split.saveState()}
        ls = []
        for i in range(split.count()):
            win = split.widget(i)
            ls.append(win)     
        dc["wins"] = ls
        dc["openedWidth"] = split.openedWidth
        return dc
    def _saveMiddle(self):
        dc = {"state" : self.middle.saveState()}
        dc["state1"] = self.middle.split.saveState()
        ls = []
        for i in range(self.middle.split.count()):
            win = self.middle.split.widget(i)
            ls.append(win)     
        dc["wins"] = ls 
        dc["openedWidth"] = self.middle.split.openedWidth
        return dc
  
    def _restoreMiddle(self, state):
        dc = state.get("middle", None)
        if dc:
            for win in dc["wins"]:
                self.addMiddle(win)
            self.middle.split.restoreState(dc.get("state1", None))
            self.middle.restoreState(dc.get("state", None))
            self.middle.split.openedWidth = (dc.get("openedWidth", 100))
    def _restoreSplit(self, state, fun, name):
        innState = state.get(name, None)  
        if innState:
            for win in innState["wins"]:
                fun(win)
            getattr(self, name).restoreState(innState["state"])   
            getattr(self, name).openedWidth = innState.get("openedWidth", 100)
            
            

