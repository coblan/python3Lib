#!python3

import sys,os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from heQt.itemView import TreeView
from heQt.itemModel import StdItemModel
from heQt.item import StdItem
from subprocess import Popen
import subprocess,threading
from heStruct.cls import sub_obj_call,add_sub_obj
from string import Template
from heQt.dockWidget import DockWidget,DockPanel
from heQt.stdoutView import StdoutView
from heQt.mainWidget import MainWidget

class myTreeView(TreeView):
    def __init__(self,*args):
        super(myTreeView,self).__init__(*args)
        self.setDragEnabled(True)
        self.info=QTextEdit()
        
        self.writLock = threading.Lock()
        self.proc = QProcess()
        self.proc.readyReadStandardOutput.connect(self.proc_stdout)
        self.proc.readyReadStandardError.connect(self.proc_stderr)
##        self.proc.readyRead.connect(self.proc_read)
##        self.que = queue.Queue()
        
        self.proc.finished.connect(self.pro_finished)
        # 设置model      
        if not os.path.exists('model'):
            mode=StdItemModel()
        else:
            with open('model','rb') as f:
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
            p.fill(QColor(i) )
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
    def proc_stdout(self):
        self.writLock.acquire()
        msg = self.proc.readAllStandardOutput().data().decode('gbk')
        if msg:
            view.write(msg)
##            self.que.put(msg)
        self.writLock.release()
##    def proc_read(self):
##        msg=self.proc.readAll().data().decode('gbk')
##        print(msg)
##        self.print_msg()
    def proc_stderr(self):
##        self.proc_stdout()
        self.proc_stdout()
        self.writLock.acquire()
        msg = self.proc.readAllStandardError().data().decode('gbk')
        
##        self.que.put('red=>'+msg)
        view.write('red=>'+msg)
        self.writLock.release()
##        self.print_msg()
        
    def pro_finished(self,*args):
        print('green=>____运行结束____')
        
##    def print_msg(self):
##        while not self.que.empty():
##            print( self.que.get() )
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

##        self.proc = Popen('cmd /c tmp.bat',universal_newlines=True,stdout= subprocess.PIPE,stderr=subprocess.PIPE,bufsize=0 )
##        self.proc_cnt=0
        
##        def loop_read(meth='stdout' ):
##            while True:
##                out=getattr(self.proc,meth).read()
##                if out:
##                    self.writLock.acquire()
##                    if meth=='stdout':
##                        print(out)
##                    elif meth == 'stderr':
##                        print('red=>'+str(out) )
##                    self.writLock.release()
##                else:
##                    self.proc_cnt+=1
##                    if self.proc_cnt==2:
##                        print( 'green=>____运行结束____' )
##                    break
####        def loop_read_erro():
####            while True:
####                out=self.proc.stderr.read()
####                if out:print('<span style="color:red"'+str(out)+'</span>')
####                else:break
##        self.thread1= threading.Thread(target=loop_read )
##        self.thread1.start()
##        self.thread2 = threading.Thread(target= loop_read,args=('stderr',))
##        self.thread2.start()
        self.proc.start('cmd /c tmp.bat')
        
    
    def save(self):
        idx=self.currentIndex()
        if idx.isValid():
            self.model().itemFromIndex(idx).setData(self.info.toPlainText(),Qt.UserRole+1)
        #self.tree.model().save('confing')
        with open('model','wb') as f:
            pickle.dump(self.model(),f)
    def get_menu(self):
        menu=QMenu(self)
        ls=[]
        if not self.underMsItem():
            menu.addActions(self.actions_map['null'])
            menu.addActions(self.actions_map['save'])
        else:
            for k in ['run','item_add','color','save']:
                if isinstance(self.actions_map[k],list):
                    menu.addActions(self.actions_map[k])
                elif isinstance(self.actions_map[k],QMenu):
                    menu.addMenu(self.actions_map[k])
                act= QAction(menu)
                act.setSeparator(True)
                menu.addAction(act)
                
        return menu
class win(QSplitter):
    def __init__(self,*args):
        super(win,self).__init__(*args)
        self.tree=myTreeView()
        self.info=self.tree.info
        self.addWidget(self.tree)
        self.addWidget(self.info)
    def save(self):
        self.tree.save()
##        stns=QSettings('stns',QSettings.IniFormat)
##        stns.setValue('win/geo',self.saveGeometry())
##        stns.setValue("win/split",self.saveState())  
        dc={}
        dc['geo'] = self.saveGeometry()
        dc['state']= self.saveState()
        return pickle.dumps(dc)
    def restore(self,dcstr):
        if not dcstr:
            return
        dc = pickle.loads(dcstr)
        self.restoreGeometry(dc['geo'])
        self.restoreState(dc['state'])
##        stns=QSettings('stns',QSettings.IniFormat)
        
##            mainWin.restoreGeometry( stns.value('win/geo') )
##            mainWin.restoreState(stns.value("win/split") )

if __name__=='__main__':
    import pickle
    
    os.chdir('cmdgui')
    app=QApplication(sys.argv)
    mid_win=win(None)
    
    mainWin=MainWidget()
    mainWin.dock=DockWidget(mainWin)
    mainWin.setCentralWidget(mainWin.dock)
    
    mainWin.dock.setCentralWidget( mid_win )    
    add_sub_obj(mainWin,mid_win)
    
    mainWin.enableSaveSession()
    mainWin.registeSaveItem(mid_win.restore,mid_win.save,'mid_win')
    
    mainWin.setWindowTitle(u'命令行界面版')
    
    mainWin.panel1=DockPanel()
    mainWin.dock.addMiddle( mainWin.panel1)
    
    view=StdoutView(mainWin)
    mainWin.panel1.addTab(view,'message')  
    
    sys.stdout=view.getStdoutObj()
    sys.stderr = sys.stdout  
      
    sys.stderr_prox=view.getStdoutObj()
    
    mainWin.restoreAll()
    mainWin.show()
##    stns=QSettings('stns',QSettings.IniFormat)

##    mainWin.restoreGeometry( stns.value('win/geo') )
##    mainWin.restoreState(stns.value("win/split") )
    

    sys.exit(app.exec_())

