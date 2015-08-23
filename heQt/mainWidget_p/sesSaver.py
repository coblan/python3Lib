#######################################################
# 导出类:

#   SesSaver  
#         : 实现保存功能的子对象类。全名意义为：session saver，会话保存器
#
#######################################################
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from heStruct.cls import sub_obj_call, add_sub_obj


    
class SesSaver(object):
    """充当Qmainwidget的功能组件，用于保存session会话。
使用步骤：
    启动时，按照顺序调用以下 函数
    1. registeSaveItem   注册 restore save name 。
                 需要随QMainwidget一起保存的子类，必须提供这三个函数。See also 该函数说明
    2. restoreAll  调用该函数恢复。
                 可以是在QMainwidget的构造函数最后调用，甚至最好在构造函数外部单独调用。总之合适的地方调用。
    """
    def __init__(self, mainWin):
        self.saveItems = []
        assert isinstance(mainWin, QMainWindow)
        self.mainWin = mainWin
        self.settings = mainWin.settings
    def closeEvent(self, event):
        self.__saveAll()
    def registeSaveItem(self, restore, save, name):
        """ 注册一项某个需要随QMainWidget状态一起保存的对象
        restore 是callable，用于恢复状态，被传入settings.value(name)值。
        save 是callable，用于保存状态时调用，值存储在settings.value(name)
        name 是 ustr,表示保存在settings里面的名字
            
        例子见本页测试部分的 testSplitter.saveItems()
        """
        self.saveItems.append((restore, save, name) )  

    def restoreAll(self):
        self.mainWin.restoreState(self.settings.value("state", b""))
        self.mainWin.restoreGeometry(self.settings.value("geometry", b""))   
        
        for item in self.saveItems:
            item[0](self.settings.value(item[2], b"") ) 
            
    def __saveAll(self):
        self.settings.setValue("state", self.mainWin.saveState())
        self.settings.setValue("geometry", self.mainWin.saveGeometry())
        
        for item in self.saveItems:
            self.settings.setValue(item[2], item[1]() )  

########################################################################

# 后面是测试用代码

#######################################################################
class MainWin(QMainWindow):
    """
A.. 保存各个对象的状态，启动时便于恢复
    1 . TPMainWin1.registeSaveItem (items) ,用该函数注册。
        items具体的形式，参看saveSesstion.registeSaveItem(self, restore, save, name)
        
    2 . TPMainWin1.restoreAll() ,恢复状态
    3 . 在退出时调用 TPMainWin1.saveAll() ,保存状态，（默认，已经在TPMainWin1.closeEvent里面已经调用了）
    """
    def __init__(self, dirBin = "bin/settings", *args):
        super().__init__( *args)
        self.settings = QSettings(dirBin, QSettings.IniFormat)
        
        # 添加保存sesstion功能
        self.saveSess = add_sub_obj(self, SesSaver(self))
        self.restoreAll = self.saveSess.restoreAll
        self.registeSaveItem = self.saveSess.registeSaveItem
        
    @sub_obj_call
    def closeEvent(self, event):
        pass
  
class testSplitter(QSplitter):
    "测试mainwin的"
    def __init__(self, *args):
        super().__init__( *args)
        self.addWidget(QWidget(self))
        self.addWidget(QPlainTextEdit(self))
    
    def saveItems(self):
        return [(self.restoreGeometry, self.saveGeometry, "splitter/geo"), 
                (self.restoreState, self.saveState, "splitter/state") ]

       

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    oo = testSplitter()
    win = MainWin()
    for i in oo.saveItems():
        win.registeSaveItem( *i)
    win.setCentralWidget(oo ) 
    win.show()
    win.restoreAll()
    sys.exit(app.exec_())