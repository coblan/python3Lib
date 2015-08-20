from PyQt5.QtWidgets import *
from heQt.itemModel import * 

class mixIn(object):
    """
*. 右键菜单显示，只需要self.addAction("do").connect(self.do)

"""
    def __init__(self,*args):
        super().__init__(*args)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openCtxMenu)
        
    def openCtxMenu(self,point):
        self.menu=QMenu(self)
        self.ctxMenuIdx=self.indexAt(point)
        self.menu.addActions(self.actions())
        self.menu.exec_(self.viewport().mapToGlobal(point))
        
    def addAction(self,act):
        "@act : str / QAction"
        if isinstance(act, str):
            act=QAction(act,self)
            QWidget.addAction(self,act)
        elif isinstance(act, QAction):
            QWidget.addAction(self,act)
        return act
    
    def itemFromIndex(self, index):
        return self.model().itemFromIndex(index)
    
    def currentItem(self):
        index=self.currentIndex()
        if index.isValid():
            return self.itemFromIndex( index )
    def underMsItem(self):
        if self.ctxMenuIdx.isValid():
            return self.itemFromIndex(self.ctxMenuIdx)
        
    def append(self,*args):
        if not self.model():
            self.setModel(StdItemModel())
        return self.model().append(*args)
    def remove(self,*args):
        self.model().remove(*args)  
        
#@fun_conect_to_ctxMenu      
class tableView(mixIn,QTableView):
    pass


#@fun_conect_to_ctxMenu
class listView(mixIn,QListView):
    pass
        
#@fun_conect_to_ctxMenu
class TreeView(mixIn,QTreeView):
    pass
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