#!python3
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys,os

from heQt.itemView import TreeView
from heQt.itemModel import StdItemModel as treeModel
from heQt.item import stdItem
from subprocess import Popen
from string import Template

class aux(QObject):
    def __init__(self, tree_,info_):
        super().__init__()
        self.tree=tree_
        self.info=info_
    def add(self):
        itm= stdItem('new item')
        itm.setData(QColor('red'),Qt.ForegroundRole)
        self.tree.append(itm,self.tree.underMsItem())
    
    def delete(self):
        item= self.tree.underMsItem()
        if item:
            if QMessageBox.information(None,'warn','realy delete?%s'%item.data())==QMessageBox.Ok:
                self.tree.model().remove(item)
    
    def run(self):
        scope={}
        exec(self.info.toPlainText(),scope)
        cmd=scope.get("cmd",None)
        if not cmd:
            print('没有发现cmd变量')
            return
        if 'var' in scope:
            cmd=Template(cmd).substitute(scope["var"])
        with open('tmp.bat','w') as f: 
            f.write(cmd)
        Popen('cmd /k tmp.bat',universal_newlines=True)
    
    def save(self):
        idx=self.tree.currentIndex()
        self.tree.model().itemFromIndex(idx).setData(self.info.toPlainText(),Qt.UserRole+1)
        #self.tree.model().save('confing')
        with open('model','bw') as f:
            pickle.dump(self.tree.model(),f)
            

class myTreeView(TreeView):
    def __init__(self,*args):
        super().__init__(*args)
        self.setDragEnabled(True)
        
    def currentChanged(self,cur,pre):
        if pre.isValid():
            self.model().itemFromIndex(pre).setData(self.info.toPlainText(),Qt.UserRole+1)
        self.info.setPlainText(cur.data(Qt.UserRole+1))
        return super().currentChanged(cur,pre)

##TreeView.currentChanged=indexChanged

class win(QSplitter):

    def closeEvent(self,evnt):
        auOb.save()
        stns=QSettings('stns',QSettings.IniFormat)
        stns.setValue('win/geo',self.saveGeometry())
        stns.setValue("win/split",self.saveState())
        QWidget.closeEvent(self,evnt)
    

if __name__=='__main__':
    import pickle
    
    os.chdir('cmdgui')
    app=QApplication(sys.argv)
    mainWin=win(None)
    mainWin.setWindowTitle('命令行界面版')

    tree=myTreeView()
    info=QTextEdit()
    auOb=aux(tree,info)
    tree.info=info
    
    if not os.path.exists('model'):
        mode=treeModel()
    else:
        with open('model','br') as f:
            mode=pickle.load(f)
    
    tree.setModel(mode)
    
    tree.addAction('run').triggered.connect(auOb.run)
    
    act=QAction(None)
    act.setSeparator(True)
    tree.addAction(act)
    tree.addAction('add').triggered.connect(auOb.add)
    tree.addAction('delete').triggered.connect(auOb.delete)
    tree.addAction('save').triggered.connect(auOb.save)
    
    mainWin.addWidget(tree)
    mainWin.addWidget(info)
    
    mainWin.show()
    stns=QSettings('stns',QSettings.IniFormat)
    mainWin.restoreGeometry(stns.value('win/geo'))
    mainWin.restoreState(stns.value("win/split"))
    

    sys.exit(app.exec_())

