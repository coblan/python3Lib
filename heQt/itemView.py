#!python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from heQt.itemModel import * 



class mixIn(object):
    """
*. 右键菜单显示，只需要self.addAction("do").connect(self.do)
2. get_menu：回调函数，返回一个Qmenu，这个menu用作右键菜单。可以更具鼠标位置的不同，返回不同的menu
"""
    def __init__(self, *args):
        """
        """
        super().__init__(*args)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.open_ctx_menu)
        self.ctxMenuIdx = None
        self.menu = None
        
    def open_ctx_menu(self, point):
        self.ctxMenuIdx = self.indexAt(point)
        self.menu = self.get_menu()
        self.menu.exec_(self.viewport().mapToGlobal(point))
        
    def addAction(self,act):
        """ << 已经用get_menu函数添加了menu，所以该函数可能被废除。

        @:type act1: QAction/str
        @param act1: Person to repress.

        """
        if isinstance(act, str):
            act=QAction(act,self)
            QWidget.addAction(self, act)
        elif isinstance(act, QAction):
            QWidget.addAction(self, act)
        return act
    
    def itemfromindex(self, index):
        return self.model().itemFromIndex(index)
    
    def currentItem(self):
        index=self.currentIndex()
        if index.isValid():
            return self.itemfromindex( index )
        
    def underMsItem(self):
        if self.ctxMenuIdx.isValid():
            return self.itemfromindex(self.ctxMenuIdx)
        
    def append(self,*args):
        if not self.model():
            self.setModel(StdItemModel())
        return self.model().append(*args)
    
    def remove(self,*args):
        self.model().remove(*args)  
        
    def get_menu(self):
        """minIn默认的返回菜单函数，该菜单用作右键菜单
        """
        menu=QMenu(self)
        menu.addActions(self.actions())
        return menu 


class TableView(mixIn, QTableView):
    pass


class ListView(mixIn, QListView):
    pass
        

class TreeView(mixIn, QTreeView):

    def autoExpand(self):
        "自动恢复上次关闭的状态，有：展开项，当前项。(只能在设置了model之后才能调用改函数)"
        self.model().treeView=self
        ls = list(self.model().walk() )
        for p,clst in ls[-1::-1]:
            if getattr(p,'p_expand',None):
                self.expand(p.index())
 
            if getattr(p,'p_selected',None):
                self.setCurrentIndex(p.index())
                
##    def append(self,data):
##        if not self.model():
##            self.setModel(treeModel())
##        return self.model().append(data)
  
#@fun_conect_to_ctxMenu
#class columnView(QColumnView,ctxMenu):
    #contextMenu=pyqtSignal(QModelIndex,QMenu)

class proBarItemDelegate(QStyledItemDelegate):
    #contextMenu=pyqtSignal(QModelIndex,QMenu)
    def __init__(self,parent=None):
        super(proBarItemDelegate,self).__init__(parent)
    def paint(self,painter,option,index):
        progressBarOption = QStyleOptionProgressBar()
        progressBarOption.rect = option.rect
        progressBarOption.minimum = 0
        progressBarOption.maximum = 100
        progressBarOption.progress = 50#index.data()
#        progressBarOption.text = "{0}%".format(progressBarOption.progress)
        progressBarOption.textVisible = True
        progressBarOption.textAlignment=Qt.AlignHCenter
        QApplication.style().drawControl(QStyle.CE_ProgressBar, progressBarOption, painter)
        QStyledItemDelegate.paint(self,painter,option,index)
        
########################
# 下面是测试代码
########################

def test():
    if win.underMsItem():
        win.underMsItem().append('jk')
    else:
        win.append("jk")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = TreeView()
    win.show()
    win.addAction("click").triggered.connect(test)
    sys.exit(app.exec_())