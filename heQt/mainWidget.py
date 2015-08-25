#######################################################
# 导出类
# MainWidget
#        视窗框架类
#######################################################
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from heStruct.cls import sub_obj_call, add_sub_obj
from heQt.mainWidget_p.sesSaver import SesSaver, testSplitter
class MainWidget(QMainWindow):
    """
    添加的功能：
    1 enableSaveSession  启动自动保存
    """
    def __init__(self, dirBin = "bin/settings", *args):
        super().__init__( *args)
        self.settings = QSettings(dirBin, QSettings.IniFormat)
        
    
    def enableSaveSession(self):
        """添加保存sesstion功能
    调用该函数后，将更新mainWidget的两个方法（直接调用SesSaver的同名方法）:
        self.restoreAll()
        self.registeSaveItem(restore, save, name)
        
    使用步骤:
    ====================
        1 mainwidget.enableSaveSession()   启用保存功能
        2 mainwidget.registeSaveItem :注册 随MainWidget一起保存的对象信息，
                      包括(restore, save, name)，
                      restore 是callable，用于恢复状态，被传入settings.value(name)值。
                      save 是callable，用于保存状态时调用，值存储在settings.value(name)
                      name 是 ustr,表示保存在settings里面的名字
                      例子见sesSaver.registeSaveItem
        3 mainwidget.restoreAll() 在合适的地方调用，例如在构造函数的最后面
        """ 
        # 防止多次调用改函数
        if not hasattr(self, "_enableSaveON"):
            self._enableSaveON = True
            
            self.saveSess = SesSaver(self)
            add_sub_obj(self, self.saveSess)

        
    @sub_obj_call
    def registeSaveItem(self, restore, save, name):
        pass
    @sub_obj_call
    def restoreAll(self):
        pass
    
    @sub_obj_call
    def closeEvent(self, event):
        pass
    

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    oo = testSplitter()
    win = MainWidget()
    win.enableSaveSession()      # 开启保存会话功能
    for i in oo.saveItems():
        win.registeSaveItem( *i)
    win.setCentralWidget(oo ) 
    win.show()
    win.restoreAll()
    sys.exit(app.exec_())