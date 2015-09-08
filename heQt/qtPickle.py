
import pickle
from PyQt5.QtWidgets import *
from PyQt5.QtCore import  *
from heStruct.cls import  add_component,component_call

class QtPickle(QObject):
    """利用这个类，直接改装Qt的python封装类。直接改装后的Qt封装类使用更加自然。
    
    QtPickle.regist_pickle(cls), 使改装对某类生效。
    
    """
    
    components=[]

    @staticmethod
    def regist_pickle(cls):
        "注册Qt的类，自动为其添加pickle功能"
        cls.__reduce__ = QtPickle.__reduce__
        cls.__setstate__ = QtPickle.__setstate__

    def __reduce__(self):
        self.pickle_dict={}
        QtPickle.real_reduce(self)
        return self.__class__,(),self.pickle_dict

    @component_call(components)
    def real_reduce(self):
        if isinstance(self,QWidget):
            self.pickle_dict['windowTitle']=self.windowTitle()
            self.pickle_dict['widgetGeo']=self.saveGeometry()

    @component_call(components)
    def __setstate__(self,state):
        args = state.pop('args',())
        if isinstance(self,QWidget ):
            self.setWindowTitle(state.get('windowTitle',''))
            self.restoreGeometry(state.get('widgetGeo',b''))


class _mainWin(QtPickle):
    QtPickle.regist_pickle(QMainWindow)
    def real_reduce(self):
        if isinstance(self,QMainWindow):
            self.pickle_dict['saveState']=self.qtobj.saveState()

    def __setstate__(self,state):
        if isinstance(self,QMainWindow):
            self.qtobj.restoreState(state.get('saveState',b''))
            
class _tabWidget(QtPickle):
    QtPickle.regist_pickle(QTabWidget)
    def real_reduce(self):
        if isinstance(self,QTabWidget):
            print('pickle tabwidget')
    def __setstate__(self,state):
        if isinstance(self,QTabWidget):
            pass


add_component(QtPickle.components,_mainWin)
add_component(QtPickle.components,_tabWidget)
QtPickle.regist_pickle(QWidget)

##-------------------

class tstWin(QTabWidget):
    def closeEvent(self, *args, **kwargs):
        with open('d:/try/testwin_pickle','bw') as f:
            pickle.dump(self,f)
        return  super().closeEvent(*args,**kwargs)
if __name__=='__main__':
    import sys,os.path
    from heQt.qtPickle import tstWin
    app= QApplication(sys.argv)
    
    if os.path.exists('d:/try/testwin_pickle'):
        with open('d:/try/testwin_pickle','br') as f:
            win=pickle.load(f)
    else:
        win = tstWin()
    win.show()

    # win.setWindowTitle('fuck you always')
    # ss = dumps(win)
    # print(ss)
    # win2 = loads(ss)
    # win2.show()
    # wawa =pickle.dumps(win2)
    # print(wawa)
    # kiss=pickle.loads(wawa)
    # kiss.show()
    sys.exit(app.exec_())