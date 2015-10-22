from heQt.qteven import *
#from heStruct.cls import add_sub_obj
if 0:
    from heQt.scintilla_p.scintilla import Scintilla
import re,pickle
#from qt_.model_.itemModel import listModel
#listModel = QStandardItemModel
from heStruct.pyeven import *
class Autocompleter(QListView):
    def __init__(self, editor):
        """用于Scintilla 的自动补全 构造函数直接 插在eidtor上面
        @editor : Scintillar的子类
        
        使用：
        1 重载initModel 设置 数据库
        2 Autocompleter.setCompKey(Qt.Key) 设置上屏的key
        3 重载autoComplet（）完成逻辑控制
        
        其他:
        1. show(),当model.rowCount() ==0 时，不显示列表框
        
        """
        s(Autocompleter, editor)
        self.editor = editor
        if 0:
            assert isinstance(self.editor, Scintilla)        

        self.setFocusPolicy(Qt.NoFocus)
        self.setEditTriggers(QListView.NoEditTriggers)
        self.hide()
        self.doubleClicked.connect(self.insertFromIndex) 
        
        # 测试用，可以更改
        #self.setShowLines(10)
        self.empty_model = QStandardItemModel()
        #self.initModel()
        self._compKeys=[Qt.Key_Return,]
        
    def setShowLines(self,number):
        lineHeight = 20
        self.resize(250,lineHeight*number)
    
    def setPrimModel(self,model):
        self.prim_model = model
    
    
    def autoComplet(self):
        pos = self.editor.currentPos()
        lastWord = self.lastWord(pos)
        
        trimPos = pos-len(lastWord)
        mt = re.match(r'^.*?\W*(\w+)\.\W*$'.encode('utf8'), self.lastText(trimPos))
        if mt:
            itms = self.prim_model.findItems(mt.group(1).decode('utf8'),Qt.MatchExactly)
            if itms and hasattr(itms[0],'md'):
                self.setModel( itms[0].md )  
            else:
                self.setModel(self.empty_model)
        else:
            self.setModel(self.prim_model)
        
        if not lastWord:
            if not mt:
                self.hide()
            else:
                self.show()
            return
        else:
           
            mtitems = self.model().findItems(lastWord.decode('utf8'),Qt.MatchStartsWith)
            mtrows=[i.row() for i in mtitems]
            if mtrows:
                row = min(mtrows)
                self.setCurrentIndex(self.model().index(row,0))
                showPos = pos - len(lastWord)
                x = self.editor.pointXFromPos(showPos)
                y = self.editor.pointYFromPos(showPos)                
                self.move(x - 25,  y + self.editor.lineHeight())
                self.show()                 
            else:
                self.hide()    
                
    def show(self):
        if self.model().rowCount() !=0:
            return s(Autocompleter)
        else:
            self.hide()
        
    def autoComplet001(self):
        "只有关键字的辅助，不包括类.方法 这种辅助"
        pos = self.editor.currentPos()
        lastWord = self.lastWord(pos)
        if not lastWord:
            self.hide()
            return
        else:
            mtitems = self.model().findItems(lastWord.decode('utf8'),Qt.MatchStartsWith)
            mtrows=[i.row() for i in mtitems]
            if mtrows:
                row = min(mtrows)
                self.setCurrentIndex(self.model().index(row,0))
                showPos = pos - len(lastWord)
                x = self.editor.pointXFromPos(showPos)
                y = self.editor.pointYFromPos(showPos)                
                self.move(x - 25,  y + self.editor.lineHeight())
                self.show()                 
            else:
                self.hide()

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
    
    def beforeKey(self, key, modifier):
        "如果要消耗掉这个 keyPress，就返回True"
        if self.isHidden():
            return
        index = self.currentIndex()
        row = index.row()
        if key == Qt.Key_Up:
            if  row> 0:
                self.setCurrentIndex(index.sibling(row - 1, 0))
            return True
        elif key == Qt.Key_Down:
            if row < self.model().rowCount():
                self.setCurrentIndex(index.sibling(row + 1, 0))
            return True
        elif key in self._compKeys and self.selectedIndexes():
            self.insertFromIndex(index)
            return True    
        elif key == Qt.Key_Escape:
            self.hide()
            return True
        
    def setCompKey(self,key):
        if key not in self._compKeys:
            self._compKeys.append(key)
        
    def afterKey(self, key, modifier):
        if not key == 0x01000021 and not modifier \
           and key != Qt.Key_Up and key != Qt.Key_Down:
            self.autoComplet()

    def lastText(self, pos):
        '返回当前位置之前，当前行的文字'
        line = self.editor.lineFromPos(pos)
        lineStart = self.editor.posFromLine(line)
        text = self.editor.textRange(lineStart, pos) 
        return text
    def lastWord(self, pos):
        text = self.lastText(pos)
        res = re.search(r"\W*?(\w*)$".encode("utf8"), text)
        if res:
            return res.group(1)
        else:
            return "".encode("utf8")

    def autoComplet22(self):
        '好像是 APDL的辅助'
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
    
    def load_toolFile(self,path):
        mp ={}
        with open(path,'rb') as f:
            mp = pickle.load(f)
        if mp:
            model = QStandardItemModel()
            for k,v in mp.items():
                item = QStandardItem(k)
                md = QStandardItemModel()
                for i in v:
                    md.appendRow(QStandardItem(i))
                item.md = md
                md.sort(0)
                model.appendRow(item)
            model.sort(0)
            self.setModel(model)
            self.prim_model = model
            
    def setup00test(self):
        self.load_toolFile('dogbit')
        self.setShowLines(10)
        #model = QStandardItemModel()
        #ls =['one','two','three','four','five','six','seven','eight','nine','ten','eleven','twle']
        #for i in ls:
            #j = QStandardItem(i)
            #j.md = QStandardItemModel()
            #j.md.appendRow(QStandardItem('ttt'))
            #model.appendRow(j)
        #model.appendRow(QStandardItem("hello"))
        #model.appendRow(QStandardItem("world") )
        #self.setPrimModel(model)
        
        
class ParseTool(object):
    def get(self,globeDict):
        self.mp={}
        for k ,v in globeDict.items():
            self.mp[k]=dir(v)
        
    def save(self,path):

        with open(path,'wb') as f:
            pickle.dump(self.mp,f)
    
    

#obj = ParseTool()
#obj.get(globals())
#obj.save('dogbit')