from heQt.qteven import *
from heStruct.cls import add_sub_obj
if 0:
    from qt_.widget.codeEditor import CodeEditor
import re
#from qt_.model_.itemModel import listModel
listModel = QStandardItemModel
class AutocompBase(QListView):
    def __init__(self, editor):
        """用于CodeEditor的自动补全 构造函数直接 插在eidtor上面
        @editor : CodeEditor的子类
        
        使用：
        1 重载initModel 设置 数据库
        2 
        """
        super().__init__( editor)
        self.editor = editor
        if 0:
            assert isinstance(self.editor, CodeEditor)        
        add_sub_obj(editor, self)
        
        self.setFocusPolicy(Qt.NoFocus)
        self.setEditTriggers(QListView.NoEditTriggers)
        self.hide()
        self.doubleClicked.connect(self.insertFromIndex) 
        
        self.initModel()
    def initModel(self):
        model = listModel()
        self.setModel(model)
        model.append("hello")
        model.append("world")   
    def autoComplet(self):
        pos = self.editor.currentPos()
        lastWord = self.lastWord(pos)
        if not lastWord:
            self.hide()
            return
        else:
            showPos = pos - len(lastWord)
            x = self.editor.pointXFromPos(showPos)
            y = self.editor.pointYFromPos(showPos)                
            self.move(x - 25,  y + self.editor.lineHeight())
            self.show()  
    def insertFromIndex(self, index):
        """双击时直接插入点击项"""
        text = index.data(Qt.DisplayRole)
        pos = self.editor.currentPos()
        lastW = self.lastWord(pos)
        
        self.editor.replaceRange(text, pos - len(lastW), len(lastW))
        self.editor.gotoPos(pos - len(lastW) + len(text))   
        self.hide()    

    def mouseClick(self, line, modifers):
        self.hide()

    def afterKey(self, key, modifier):
        if not key == 0x01000021 and not modifier:
            self.autoComplet()
            #self.normalAutoComp()

           
    def lastWord(self, pos):
        line = self.editor.lineFromPos(pos)
        lineStart = self.editor.posFromLine(line)
        text = self.editor.textRange(lineStart, pos)
        res = re.search(r"\W(\w*)$".encode("utf8"), text)
        if res:
            return res.group(1)
        else:
            return "".encode("utf8")

    def autoComplet22(self):
        pos = self.editor.currentPos()
        line = self.editor.lineFromPos(pos)
        lineStart = self.editor.posFromLine(line)
        text = self.editor.textRange(lineStart, pos)
        
        if re.search(",".encode("utf8"), text):
            self.setModel(self.editor.lexer.autoFreeProxy)
        else:
            self.setModel(self.autoFunModel)
        #self.normalAutoComp()     
        mainWin = QApplication.instance().mainWin
        if mainWin.infoState == "normal":
            self.normalAutoComp()
            #self.extraInfoViewFun()
        elif mainWin.infoState == "none":
            self.hide()  
        
        