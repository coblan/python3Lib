"""
导出类为：
StdoutView

"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys,re

class StdoutView(QTextBrowser):
    """
    例子
    =============
    
    1. 快捷的设置sys.stdout对象
    win=StdoutView()
    sys.stdout=win.getStdoutObj()
    sys.stderr = sys.stdout
    
    2. 设置定时探针,n秒显示一次探针的值
    win.openSensor(5)  /win.openSensor_notCThread(5)          # 普通/非创建线程中启动 sensor
    doSometing ...
    win.sensorValue=“要显示的内容"
    doSomething ...
    win.closeSensor()  /win.closeSensor_notCThread()          # 普通/非创建线程中关闭 sensor
    """
    
    openSensor_notCThread = pyqtSignal(int)
    closeSensor_notCThread = pyqtSignal()

    def __init__(self,*args):
        super(StdoutView,self).__init__(*args)
        self.sensorValue = "StdoutView default sensor"
        self.openSensor_notCThread.connect(self.openSensor)    # 但在非创建线程开启定时探测时，因为timer不能在 
        self.closeSensor_notCThread.connect(self.closeSensor)  # 非创建线程 启动，所以要利用signal来启动timer
        
        actNames = ["copy", "clear"]
        for name in actNames:
            act = QAction(name, self)
            self.addAction(act)
            act.triggered.connect(getattr(self, name))

        self.setContextMenuPolicy(Qt.ActionsContextMenu)

    def setAdaptor(self,adapt):
        if hasattr(self,'adaptor'):
            self.adaptor.cout.disconnect()
        self.adaptor=adapt
        self.adaptor.cout.connect(self.write)
        
    def write(self,msg):
        """之所有用insertPlainText，（还需要自己控制滚动条，那么麻烦）是因为append会把输入当成html，如果遇到输出中有<>号，就
        无法显式，此外append也会多一个回车。
        """
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)

        start = 0
        for mt in re.finditer(r'^(\w+)=>(.*)<=END$',msg,re.M ):
            end = mt.start()
            self.setTextColor(QColor('black'))
            self.insertPlainText(msg[start:end])

            start = end
            end = mt.end()
            self.setTextColor(QColor(mt.group(1)))
            self.insertPlainText(mt.group(2))

            start = end
        self.setTextColor(QColor('black'))
        self.insertPlainText(msg[start:])
        # if rt :
        #     self.setTextColor(QColor(rt. group(1)))
        #     self.insertPlainText(rt.group(2))
        #
        # else:
        #     self.setTextColor(QColor('black'))
        #     self.insertPlainText(msg)
            
        bar=self.verticalScrollBar()
        bar.setSliderPosition(bar.maximum ())

    def getStdoutObj(self):
        """快捷的方式，返回一个stdoutAdaptor对象。可以多次的调用，返回的都是同一个adapter。
        单线程时，可以直接用:sys.stdout = self .多线程时，必须使用该函数返回的obj。"""
        if not hasattr(self, 'adaptor'):
            self.setAdaptor(StdoutAdaptor())
        return self.adaptor

    def openSensor(self, sec):
        "开启传感器,sec秒显示一次 值"
        sec = sec * 1000
        self.closeSensor()
        self._sensorTimer = self.startTimer(sec)
        
    def closeSensor(self):
        if hasattr(self, "_sensorTimer"):
            self.killTimer(self._sensorTimer)

    def timerEvent(self, e):
        if hasattr(self, "_sensorTimer", ) and e.timerId() == self._sensorTimer:
            print(self.sensorValue)
    
class StdoutAdaptor(QObject):
    cout=pyqtSignal(str)
    def __init__(self,*args):
        super(StdoutAdaptor,self).__init__(*args)
    
    def write(self,arg):
        self.cout.emit(arg)  

        
class syntex(QSyntaxHighlighter):
    def __init__(self,*args):
        super(syntex,self).__init__(*args)
        self.keyword=re.compile('warning|ERROR|SEVERE',re.I)
    def highlightBlock(self,text):
        for ii in re.finditer(self.keyword,text):
            form=QTextCharFormat()
            form.setForeground(Qt.red)
            self.setFormat(ii.start(),ii.end()-ii.start(),form) 
        
if __name__=='__main__':
    app=QApplication(sys.argv)
    
    win=StdoutView()
    win.show()
    stdout=StdoutAdaptor()
    win.setAdaptor(stdout)
    
    sys.stdout=stdout
    
    sys.exit(app.exec_())