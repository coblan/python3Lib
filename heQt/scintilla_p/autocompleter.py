# -*- encoding:utf8 -*-
from heQt.qteven import *
#from heStruct.cls import add_sub_obj
if 0:
    from heQt.scintilla_p.scintilla import Scintilla
import re,pickle

from heStruct.pyeven import *

class Autocompleter(QListView):
    wordspattern = re.compile(r'\s*\.*\s*(\w+|\.)$'.encode('utf8'))
    def __init__(self, editor):
        """用于Scintilla 的自动补全 构造函数直接 插在eidtor上面
        @editor : Scintillar的子类
        
        使用：
        1 setAutoModel(AutoModel()) 设置 数据库。所有的model控制逻辑，在AutoModel对象中来实现。
        2 Autocompleter.setCompKey(Qt.Key) 设置上屏的key
        3 重载autoComplet（）完成逻辑控制。当前实现，比较好的匹配和AutoModel类对象的getModel()方法
        
        其他:
        1. showWithPos(),根据输入位置，显示提示框
        2. setShowLines(10) ,提示框显示多少行
        
        """
        s(Autocompleter, editor)
        if 0:
            assert isinstance(editor, Scintilla)    
        self.editor = editor
        self._autoModel = None
        self._compKeys=[Qt.Key_Return,]
        
        self.setFocusPolicy(Qt.NoFocus)
        self.setEditTriggers(QListView.NoEditTriggers)
        self.hide()
        
        self.doubleClicked.connect(self.insertFromIndex) 
        
    def setShowLines(self,number):
        lineHeight = 20
        self.resize(250,lineHeight*number)
    
    def setAutoModel(self,model):
        self._autoModel = model
    
    def autoComplet(self):
        pos = self.editor.currentPos()
        text = self.lastText(pos)
        out = []
        while True:
            mt = Autocompleter.wordspattern.search(text)
            if mt:
                out.append(mt.group(1))
                text = text[:mt.start()]
            else:
                break
        out.reverse()
        out = [i.decode('utf8') for i in out]
        print(out)
        if self._autoModel:
            md ,row,needSetModel = self._autoModel.getModel(out)
            if md:
                if needSetModel:
                    self.setModel(md)
                self.setCurrentIndex(self.model().index(row,0) )
                self.showWithPos(pos)
            else:
                self.hide()
     
    def showWithPos(self,pos):
        lastWord = self.lastWord(pos)
        showPos = pos - len(lastWord)
        x = self.editor.pointXFromPos(showPos)
        y = self.editor.pointYFromPos(showPos)                
        self.move(x - 25,  y + self.editor.lineHeight())
        self.scrollTo(self.currentIndex(), QAbstractItemView.PositionAtTop)
        self.show()   
        
        
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
    

            
    def setup00test(self):
        automodel = AutoModel()
        automodel.load_toolFile('dogbit')
        self.setAutoModel(automodel)
        self.setShowLines(10)

    def setup001(self, path):
        automodel = AutoModel()
        automodel.load_toolFile(path)
        self.setAutoModel(automodel)
        self.setShowLines(10)        

class AutoModel(object):
    def __init__(self):
        #self._listView = listView
        self._primModel = None
        self._lastls= []
        self._crtModel= None
        self._crtItem = None
        
    def getModel(self, ls):
        """最重要的是理解发送过来的ls的样子，ls是文字列表
        如果输入：dog.pig
        ls =[dog,pig]
        如果输入：dog.pig.
        ls = [dog,pig,'.']
        注意，有.号。
        
        """
        row=0
        needSetModel = False
        if not ls or ls[0]=='.':
            self._lastls = ls
            self._crtItem =None
            self._crtModel =None
            return None,row,None
        if len(ls)==1:
            self._crtModel = self._primModel  
            if not self._lastls:
                needSetModel = True
                
        elif self._lastls != ls[:-1]:
            needSetModel = True  
                #needSetModel = True
                #item = self._crtModel.itemFromIndex( self._listView.currentIndex() )
            self._crtItem = self.getChainItem(ls[:-1])
            if hasattr(self._crtItem,'md'):
                md = self._crtItem.md
                if isinstance(md,list):
                    model = QStandardItemModel()
                    for i in md:
                        item = QStandardItem(i)
                        model.appendRow(item)
                    #model = QStringListModel()
                    #model.setStringList(md)
                    self._crtItem.md = model
                self._crtModel = self._crtItem.md
            
        mtitems = self._crtModel.findItems(ls[-1],Qt.MatchStartsWith)
        mtrows=[i.row() for i in mtitems]
        if mtrows:
            row = min(mtrows)
            #self._listView.setCurrentIndex(self._crtModel.index(row,0))   
            self._crtItem = self._crtModel.item(row)
        
        self._lastls = ls
        return self._crtModel,row,needSetModel
    
    def getChainItem(self, ls):
        "根据文字列表，从primModel开始查找相应的item项"
        if self._primModel:
            md = self._primModel
            item = None
            for i in ls:
                items = md.findItems(i,Qt.MatchExactly)
                if items and hasattr( items[0] ,'md'):
                    md= items[0].md
                    item = items[0]
                else:
                    break
            return item
                
                    
                
    def load_toolFile(self,path):
        mp ={}
        with open(path,'rb') as f:
            mp = pickle.load(f)
        if mp:
            model = QStandardItemModel()
            for k,v in mp.items():
                item = QStandardItem(k)
                #md = QStandardItemModel()
                #for i in v:
                    #md.appendRow(QStandardItem(i))
                item.md = v
                #md.sort(0)
                model.appendRow(item)
            model.sort(0)
            #self.setModel(model)
            self._primModel = model
            
