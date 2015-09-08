#!python3

import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from heQt.itemView import TreeView
from heQt.itemModel import StdItemModel
from heQt.item import StdItem
from subprocess import Popen
import subprocess, threading
from heStruct.cls import sub_obj_call, add_sub_obj
from string import Template
from heQt.dockWidget import DockWidget, DockPanel
from heQt.stdoutView import StdoutView
from heQt.mainWidget import MainWidget


class myTreeView(TreeView):
    def __init__(self, *args):
        super(myTreeView, self).__init__(*args)
        #        self.setDragEnabled(True)
        self.info = QTextEdit()

        # 生成外部process，以及process打印子模块
        self.proc = QProcess()
        self.proc_print = proc_print(self.proc)

        # 设置model
        if not os.path.exists('model'):
            mode = StdItemModel()
        else:
            with open('model', 'rb') as f:
                mode = pickle.load(f)
        self.setModel(mode)

        # 自动恢复上次关闭的状态，有：展开项，当前项。(只能在设置了model之后才能调用改函数)
        self.autoExpand()

        # 生成右键菜单子模块
        self._menu = tree_menu(self)
        
        ##        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)  # QAbstractItemView.DragDrop)
        self.setDragDropOverwriteMode(False)
    
    def get_menu(self):
        return self._menu.get_menu()
    
    def changItemColor(self):
        if self.underMsItem():
            self.underMsItem().setData(QColor(self.sender().text()), Qt.ForegroundRole)

    def currentChanged(self, cur, pre):
        "当切换treeView中的项时，保存右边的内容"
        if pre.isValid():
            self.model().itemFromIndex(pre).setData(self.info.toPlainText(), Qt.UserRole + 1)
        self.info.setPlainText(cur.data(Qt.UserRole + 1))
        return super(myTreeView, self).currentChanged(cur, pre)

    def add(self):
        itm = QStandardItem('new item')
        self.append(itm, self.underMsItem())

    def delete(self):
        item = self.underMsItem()
        if item:
            if QMessageBox.information(None, 'warn', 'realy delete?%s' % item.data()) == QMessageBox.Ok:
                self.model().remove(item)

    def run(self):
        """运行命令，这个是最重要的函数"""
        scope = {}
        try:
            exec(self.info.toPlainText(), scope)
        except Exception as e:
            print('red=>' + str(e)+'<=END')
        cmd = scope.get("cmd", None)
        if not cmd:
            print('red=>没有发现cmd变量<=END')
            return
        if 'var' in scope:
            cmd = Template(cmd).substitute(scope["var"])
        with open('tmp.bat', 'w') as f:
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
        idx = self.currentIndex()
        if idx.isValid():
            self.model().itemFromIndex(idx).setData(self.info.toPlainText(), Qt.UserRole + 1)
        # self.tree.model().save('confing')
        with open('model', 'wb') as f:
            pickle.dump(self.model(), f)


class tree_menu(object):
    def __init__(self, tree):
        self.tree = tree
        # 设置按钮组--------------------
        self.actions_map = {'run': [('run', self.run), ],
                            'null': [(u'添加', self.add), ],
                            'item_add': [(u'添加', self.add),
                                         (u'删除', self.delete), ],
                            'save': [(u'保存', self.save), ]
                            }
        for k, v in self.actions_map.items():
            ls = []
            for k1, v1 in v:
                act = QAction(k1, self.tree)
                act.triggered.connect(v1)
                ls.append(act)
            self.actions_map[k] = ls

        # 设置 menu组，这些不能在前面的 action中循环生成
        colorMenu = QMenu(u'着色', self.tree)
        for i in ['red', 'black', 'yellow', 'green']:
            act = QAction(i, colorMenu)
            p = QPixmap(QSize(50, 50))
            p.fill(QColor(i))
            act.setIcon(QIcon(p))
            colorMenu.addAction(act)
            act.triggered.connect(self.changItemColor)
        self.actions_map.update({'color': colorMenu,
                                })
        
    def get_menu(self):
        menu = QMenu(self.tree)
        ls = []
        if not self.underMsItem():
            menu.addActions(self.actions_map['null'])
            menu.addActions(self.actions_map['save'])
        else:
            for k in ['run', 'item_add', 'color', 'save']:
                if isinstance(self.actions_map[k], list):
                    menu.addActions(self.actions_map[k])
                elif isinstance(self.actions_map[k], QMenu):
                    menu.addMenu(self.actions_map[k])
                act = QAction(menu)
                act.setSeparator(True)
                menu.addAction(act)

        return menu

    def __getattr__(self, name):
        return getattr(self.tree, name)


class proc_print(object):
    """打印外部进程。此类对象作为myTreeView中的子功能模块使用"""

    def __init__(self, proc):
        self.writeLock = threading.Lock()
        self.proc = proc
        self.proc.readyReadStandardOutput.connect(self.proc_stdout)
        self.proc.readyReadStandardError.connect(self.proc_stderr)
        self.proc.finished.connect(self.pro_finished)

    def proc_stdout(self):
        self.writeLock.acquire()
        byt = self.proc.readAllStandardOutput().data()
        try:
            msg = byt.decode('utf8')
        except UnicodeDecodeError:
            msg = byt.decode('gbk',errors='replace')
        print(msg)
        self.writeLock.release()

    def proc_stderr(self):
        self.writeLock.acquire()
        byt=self.proc.readAllStandardError().data()
        try:
            msg=byt.decode()
        except UnicodeDecodeError:
            msg = byt.decode('gbk',errors='replace')
        print('red=>'+msg+'<=END')
        self.writeLock.release()

    #        self.print_msg()

    def pro_finished(self, *args):
        print('green=>____运行结束____<=END')


class win(QSplitter):
    def __init__(self, *args):
        super(win, self).__init__(*args)
        self.tree = myTreeView()
        self.info = self.tree.info
        self.addWidget(self.tree)
        self.addWidget(self.info)

    # @property
    def save(self):
        self.tree.save()
        ##        stns=QSettings('stns',QSettings.IniFormat)
        ##        stns.setValue('win/geo',self.saveGeometry())
        ##        stns.setValue("win/split",self.saveState())
        dc = {}
        dc['geo'] = self.saveGeometry()
        dc['state'] = self.saveState()
        return pickle.dumps(dc)

    def restore(self, dcstr):
        if not dcstr:
            return
        dc = pickle.loads(dcstr)
        self.restoreGeometry(dc['geo'])
        self.restoreState(dc['state'])


##        stns=QSettings('stns',QSettings.IniFormat)

##            mainWin.restoreGeometry( stns.value('win/geo') )
##            mainWin.restoreState(stns.value("win/split") )

if __name__ == '__main__':
    import pickle

    os.chdir('cmdgui')
    app = QApplication(sys.argv)
    mid_win = win(None)

    mainWin = MainWidget()
    mainWin.dock = DockWidget(mainWin)
    mainWin.setCentralWidget(mainWin.dock)

    mainWin.dock.setCentralWidget(mid_win)
    add_sub_obj(mainWin, mid_win)

    mainWin.enableSaveSession()
    mainWin.registeSaveItem(mid_win.restore, mid_win.save, 'mid_win')

    mainWin.setWindowTitle(u'命令行界面版')

    mainWin.panel1 = DockPanel()
    mainWin.dock.addMiddle(mainWin.panel1)

    view = StdoutView(mainWin)
    mainWin.panel1.addTab(view, 'message')

    sys.stdout = view.getStdoutObj()
    sys.stderr = sys.stdout

##    sys.stderr_prox = view.getStdoutObj()

    mainWin.restoreAll()
    mainWin.show()

    sys.exit(app.exec_())
