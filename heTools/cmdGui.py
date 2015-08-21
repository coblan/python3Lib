# -*- encoding:utf8 -*-
from PySide.QtGui import *
from PySide.QtCore import *
import sys,os

from heQt.itemView import TreeView
from heQt.itemModel import StdItemModel
from heQt.item import StdItem
from subprocess import Popen
from string import Template

class Aux(object):
      
    def add(self):
        itm= StdItem('new item')
        self.append(itm,self.underMsItem())
    
    def delete(self):
        item= self.underMsItem()
        if item:
            if QMessageBox.information(None,'warn','realy delete?%s'%item.data())==QMessageBox.Ok:
                self.model().remove(item)
    
    def run(self):
        """运行命令，这个是最重要的函数"""
        scope={}
        exec(self.info.toPlainText(),scope)
        cmd=scope.get("cmd",None)
        if not cmd:
            print(u'没有发现cmd变量')
            return
        if 'var' in scope:
            cmd=Template(cmd).substitute(scope["var"])
        with open('tmp.bat','w') as f: 
            f.write(cmd)
        Popen('cmd /k tmp.bat',universal_newlines=True)
    
    def save(self):
        idx=self.currentIndex()
        if idx.isValid():
            self.model().itemFromIndex(idx).setData(self.info.toPlainText(),Qt.UserRole+1)
        #self.tree.model().save('confing')
        with open('model','w') as f:
            pickle.dump(self.model(),f)
            
def get_menu_fo(win):
    menu=QMenu(win)
    ls=[]
    if not win.underMsItem():
        menu.addActions(win.actions_map['null'])
        menu.addActions(win.actions_map['save'])
    else:
        for k in ['run','item_add','color','save']:
            if isinstance(win.actions_map[k],list):
                menu.addActions(win.actions_map[k])
            elif isinstance(win.actions_map[k],QMenu):
                menu.addMenu(win.actions_map[k])
            act= QAction(menu)
            act.setSeparator(True)
            menu.addAction(act)
            
    return menu

class myTreeView(Aux,TreeView):
    def __init__(self,*args):
        super(myTreeView,self).__init__(*args)
        self.setDragEnabled(True)
        self.info=QTextEdit()
        
        # 设置model
        if not os.path.exists('model'):
            mode=StdItemModel()
        else:
            with open('model','r') as f:
                mode=pickle.load(f)

        self.setModel(mode)  
        
        # 自动恢复上次关闭的状态，有：展开项，当前项。(只能在设置了model之后才能调用改函数)
        self.autoExpand()
        
        # 设置按钮组--------------------
        self.actions_map={'run':[('run',self.run),],
                          'null':[(u'添加',self.add),],
                          'item_add':[(u'添加',self.add),
                                      (u'删除',self.delete),],
                          'save':[(u'保存',self.save),]
                          }
        for k,v in self.actions_map.items():
            ls=[]
            for k1,v1 in v:
                act=QAction(k1,self)
                act.triggered.connect(v1)
                ls.append(act)
            self.actions_map[k]=ls     
        
        # 设置 menu组，这些不能在前面的 action中循环生成
        colorMenu=QMenu(u'着色',self)
        for i in ['red','black','yellow','green']:
            act= QAction(i,colorMenu)
            p=QPixmap(QSize(50,50))
            p.fill(i)
            act.setIcon(QIcon(p))
            colorMenu.addAction(act)
            act.triggered.connect(self.changItemColor)
        self.actions_map.update({'color':colorMenu,
        })
        # 设置按钮组-------------------
        
    def changItemColor(self):
        if self.underMsItem():
            self.underMsItem().setData( QColor(self.sender().text()),Qt.ForegroundRole)
    def currentChanged(self,cur,pre):
        if pre.isValid():
            self.model().itemFromIndex(pre).setData(self.info.toPlainText(),Qt.UserRole+1)
        self.info.setPlainText(cur.data(Qt.UserRole+1))
        return super(myTreeView,self).currentChanged(cur,pre)



class win(QSplitter):
    def __init__(self,*args):
        super(win,self).__init__(*args)
        self.tree=myTreeView(get_menu_fo)
        self.info=self.tree.info
        self.addWidget(self.tree)
        self.addWidget(self.info)      
            
    def closeEvent(self,evnt):
        self.tree.save()
        stns=QSettings('stns',QSettings.IniFormat)
        stns.setValue('win/geo',self.saveGeometry())
        stns.setValue("win/split",self.saveState())
        QWidget.closeEvent(self,evnt)
    

if __name__=='__main__':
    import pickle
    
    os.chdir('cmdgui')
    app=QApplication(sys.argv)
    mainWin=win(None)
    mainWin.setWindowTitle(u'命令行界面版')

    mainWin.show()
    stns=QSettings('stns',QSettings.IniFormat)

    mainWin.restoreGeometry( stns.value('win/geo') )
    mainWin.restoreState(stns.value("win/split") )
    

    sys.exit(app.exec_())

