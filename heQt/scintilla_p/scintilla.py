import sys
from heQt.qteven import *
from heQt.scintilla_p.bridge import Bridge
from heQt.scintilla_p import const
from heStruct.pyeven import *
from heQt.scintilla_p.lineManager import LineManager
from heQt.scintilla_p.autocompleter import *
from ctypes import Structure, c_int
from heQt.scintilla_p.cusLexer import CusLexer

class Scintilla(Bridge):
    """

    关键字高亮：
        style设置：相当于editor的内部环境。可以用封装过的函数设置style:
            setForeColor(n,QColor)
            setBackColor(n,Qcolor)
            setStyleFont(n,Qfont)
            其中样式标号n：32是默认格式编号。33是行面板，其他为自定义标号。这些标号用来设置文字的格式。见下面的format设置

        format设置：用样式标号n来设置关键字的格式。一般在Lexer中完成该步骤。
            setFormat(start, end, n) 少量设置格式，建议不用这个函数
            setFormatList(ranges, comments) ，参数ranges是[(start,end,n),]形式的列表。comments=[1,2,3]指出的是comment的样式标号列表
                该函数便于大量的设置关键字的格式。需要comments标号列表的原因是为了不在注释中高亮关键字。

        综上，步骤为
        1. 设置editor的style （可以在Lexer中来设置），先设置32默认格式，然后调用 Scintilla.send(const.SCI_STYLECLEARALL)/Scintilla.extendDefaultStyle()，
           让所有格式都与默认格式一致。然后再来设置其他格式。
        2. 在Lexer中解析的时候设置关键字高亮
        3. Scintilla.setLexer(Lexer)
        
        """  
    
    def __init__(self,parent=None):
        s(Scintilla,parent)
        self.send(const.SCI_SETCODEPAGE, const.SC_CP_UTF8)
        #self.setAutoIndent(True)
        self.send(const.SCI_SETLEXER, const.SCLEX_NULL)
    
        self.send(const.SCI_SETWRAPMODE, const.SC_WRAP_WORD)
        self.send(const.SCI_SETWRAPINDENTMODE, const.SC_WRAPINDENT_SAME)
        self.send(const.SCI_SETTABWIDTH, 4)
        self.send(const.SCI_SETMODEVENTMASK, const.SC_MOD_BEFOREDELETE | const.SC_MOD_BEFOREINSERT | const.SC_MOD_INSERTTEXT | const.SC_MOD_DELETETEXT)
        self.send(const.SCI_SETMARGINWIDTHN, 1, 0)
    
        self.lineManager = LineManager(self)    
        self._lexer = None
        self._autoCompleter = None
        self._extraHight = None
        
    def setLexer(self,lexer):
        self._lexer = lexer
        
    def setAutoIndent(self,b):
        self.__autoIndent = b
    def autoIndent(self):
        return self.__autoIndent
    
    def afterKey(self, key, modifier):
        if self.autoIndent():
            self.__autoIndentHandle(key, modifier)   
        if self._autoCompleter:
            self._autoCompleter.afterKey(key,modifier)        
            
    def __autoIndentHandle(self, key, modifiers):
        if  key ==Qt.Key_Return and  modifiers==Qt.NoModifier :
            line = self.currentLine()
            if line >0:
                indent = self.lineIndentation(line-1)
                self.insertText(-1, " " *indent)
                self.gotoPos(self.currentPos()+indent)
                
    def grabLine(self, line):
        """返回一个obj是lineManager.GrabLine对象。
        obj.line属性表示行数，该行数是跟随文档变化而刷新的。
        设置回调函数obj.afterLineDel=fun()，可以监视某行被删除
        """
        return self.lineManager.grabLine(line)
    
    def doubleClick(self, pos , line):
        if self._extraHight and hasattr(self._extraHight,'doubleClick'):
            self._extraHight.doubleClick(pos, line)
            
    def setExtraHight(self,obj):
        self._extraHight = obj
        
    def lineFromPos(self, pos):
        return self.send(const.SCI_LINEFROMPOSITION, pos)
    def posFromLine(self, line):
        return self.send(const.SCI_POSITIONFROMLINE, line)
    def lineLen(self, line):
        return self.send(const.SCI_LINELENGTH, line)
    def lineCount(self):
        return self.send(const.SCI_GETLINECOUNT)
    def lineIndentation(self, line):
        return self.send(const.SCI_GETLINEINDENTATION, line)
    def currentPos(self):
        return self.send(const.SCI_GETCURRENTPOS)
    def currentLine(self):
        return self.lineFromPos(self.currentPos())
    def insertText(self, pos, text):
        if isinstance(text, str):
            text = text.encode("utf8")
        self.send(const.SCI_INSERTTEXT, pos, text)
    def gotoPos(self, pos):
        self.send(const.SCI_GOTOPOS, pos)
    def setBackColor(self, n, color):
        color = QcolorToRGB(color)
        self.send(const.SCI_STYLESETBACK, n, color)
    def setForeColor(self, n, color):
        color = QcolorToRGB(color)
        self.send(const.SCI_STYLESETFORE, n, color)
    def setStyleFont(self, n, font):
        assert isinstance(font, QFont)
        self.send(const.SCI_STYLESETBOLD, n, 1 if font.bold() else 0)
        self.send(const.SCI_STYLESETITALIC, n, 1 if font.italic() else 0)
        self.send(const.SCI_STYLESETWEIGHT, n, font.weight())
        self.send(const.SCI_STYLESETSIZE, n, font.pointSize())
        self.send(const.SCI_STYLESETFONT, n, font.family().encode("utf8"))
    def setFormat(self, start, end, n):
        """少量设置高亮，建议使用setFormatList替代"""
        #tmp = self.send(SCI_GETENDSTYLED)
        
        self.send(const.SCI_STARTSTYLING, start)
        self.send(const.SCI_SETSTYLING, end - start, n)
        
        #self.send(SCI_STARTSTYLING, tmp)
    def setText(self, string):
        if isinstance(string, str):
            text = string.encode("utf8")
        elif isinstance(string, bytes):
            text = string
        else:
            return
        self.send(const.SCI_SETTEXT, 0, text)
        
    def setFormatList(self, ranges, comments = []):
        """ranges是[(start,end,n),]形式的列表
        comments是[0,1,2,3,4]这样的列表，表明comment的标号。它不会影响正常的comment的设置"""
        tmp = self.send(const.SCI_GETENDSTYLED)
        c_ranges = (c_range * len(ranges))( *ranges)
        c_comments = (c_int * len(comments))( *comments)
        super().setFormatList(c_ranges,  c_comments)
        self.send(const.SCI_STARTSTYLING, tmp)
        
    def setReadOnly(self, bool_):
        
        self.send(const.SCI_SETREADONLY, 1 if bool_ else 0)
        self.send(const.SCI_SETCARETWIDTH, 0 if bool_ else 1)
    def readOnly(self):
        return self.send(const.SCI_GETREADONLY)
    
    def extendDefaultStyle(self):
        """将默认样式32传递到所有 style Number上"""
        self.send(const.SCI_STYLECLEARALL)
    
    def isModified(self):
        return self.send(const.SCI_GETMODIFY)
    def setSavePoint(self):
        self.send(const.SCI_SETSAVEPOINT)
        self.send(const.SCI_EMPTYUNDOBUFFER)  
        
    def showNumPanel(self, boolv = True, width = 40):
        if boolv:
            self.send(const.SCI_SETMARGINTYPEN, 0, 1)
            self.send(const.SCI_SETMARGINWIDTHN, 0, width)
        else:
            self.send(const.SCI_SETMARGINWIDTHN, 0, 0)    
    def onModify(self, type_, pos, length, linesAdd, text, line, foldNow, foldPre):
        "CALLBACK"
        if type_ & const.SC_MOD_BEFOREDELETE:
            self.contentChanged('beforeDel', pos, length)
        elif type_ & const.SC_MOD_BEFOREINSERT:
            self.contentChanged('beforeInsert', pos, length)
            
        elif type_ & const.SC_MOD_INSERTTEXT:
            self.contentChanged('insert', pos, length)

        elif type_ & const.SC_MOD_DELETETEXT:
            self.contentChanged('delete', pos, length)
 
            
    def contentChanged(self,type_, pos, length):
        """
        type_:beforeDel
              beforeInsert
              insert
              delete
        """
        if not self._lexer:
            return
        if type_ == 'insert':
            self._lexer.insertEvent(pos, length)
        elif type_ =='delete':
            self._lexer.deleteEvent(pos, length)
    
    def setAutoCompleter(self, comp):
        self._autoCompleter = comp
        

    
    def grabLine(self, line):
        """返回一个obj是lineManager.GrabLine对象。
        obj.line属性表示行数，该行数是跟随文档变化而刷新的。
        设置回调函数obj.afterLineDel=fun()，可以监视某行被删除
        """
        return self.lineManager.grabLine(line)    
    
    def setBackColor(self, n, color):
        color = QcolorToRGB(color)
        self.send(const.SCI_STYLESETBACK, n, color)
        
    def setForeColor(self, n, color):
        color = QcolorToRGB(color)
        self.send(const.SCI_STYLESETFORE, n, color)
        
    #def setBold(self,n, b):
        #self.send(const.SCI_STYLESETBOLD, n ,b)
        
    def setStyleFont(self, n, font):
        assert isinstance(font, QFont)
        self._crtFont = font
        self.send(const.SCI_STYLESETBOLD, n, 1 if font.bold() else 0)
        self.send(const.SCI_STYLESETITALIC, n, 1 if font.italic() else 0)
        self.send(const.SCI_STYLESETWEIGHT, n, font.weight())
        self.send(const.SCI_STYLESETSIZE, n, font.pointSize())
        self.send(const.SCI_STYLESETFONT, n, font.family().encode("utf8"))
    def getStyleFont(self):
        return self._crtFont
        
    def setFormat(self, start, end, n):
        """少量设置高亮，建议使用setFormatList替代"""
        self.send(const.SCI_STARTSTYLING, start)
        self.send(const.SCI_SETSTYLING, end - start, n)    
    def pointXFromPos(self, pos):
        return self.send(const.SCI_POINTXFROMPOSITION, 0, pos)
    def pointYFromPos(self, pos):
        return self.send(const.SCI_POINTYFROMPOSITION, 0, pos)
    def lineHeight(self):
        """所有行都是一样高的"""
        return self.send(const.SCI_TEXTHEIGHT, 0)
    
    def getTextLength(self):
        return self.send(const.SCI_GETTEXTLENGTH)
    def getStyleAt(self, pos):
        """返回某pos处的style number"""
        return self.send(const.SCI_GETSTYLEAT, pos)   
    
    def replaceRange(self, text, pos, len_):
        """@text : utf8"""
        self.send(const.SCI_BEGINUNDOACTION)
        self.send(const.SCI_DELETERANGE, pos, len_)
        self.insertText(pos, text)
        self.send(const.SCI_ENDUNDOACTION)  
    
    def mouseClick(self, line, modifier):
        if self._autoCompleter:
            self._autoCompleter.mouseClick(line,modifier)
            
    def beforeKey(self, key, modifier):
        if self._autoCompleter:
            return self._autoCompleter.beforeKey(key, modifier)
    
    def setCaretLineShowAlways(self,b):
        self.send(const.SCI_SETCARETLINEVISIBLEALWAYS,1 if b else 0)
    def setCaretLineBack(self,color):
        # 先启动光标行高亮功能
        self.send(const.SCI_SETCARETLINEVISIBLE,1)
        # 设置背景色
        tmpcolor = QcolorToRGB(color)
        self.send(const.SCI_SETCARETLINEBACK,tmpcolor)
        # 设置透明度
        alpha = color.alpha()
        self.send(const.SCI_SETCARETLINEBACKALPHA,alpha)
        
    def setMultiCaret(self,b):
        self.send(const.SCI_SETMULTIPLESELECTION, 1 if b else 0)
        self.send(const.SCI_SETADDITIONALSELECTIONTYPING, 1 if b else 0)
        

    def getSelection(self):
        num= self.send(const.SCI_GETSELECTIONS)
        out = []
        for i in range(num):
            start = self.send(const.SCI_GETSELECTIONNSTART, i)
            end = self.send(const.SCI_GETSELECTIONNEND ,i)
            out.append((start,end))
        return out
    
    def addSelection(self,start, end):
        self.send(const.SCI_ADDSELECTION, start, end)
    
    def getMainSelection(self):
        i = self.send(const.SCI_GETMAINSELECTION)
        start = self.send(const.SCI_GETSELECTIONNSTART, i)
        end = self.send(const.SCI_GETSELECTIONNEND ,i) 
        return start,end


    def setSelBack(self,color):
        color = QcolorToRGB(color)
        self.send(const.SCI_SETSELBACK,1, color)
    def setSelFore(self,color):
        color = QcolorToRGB(color)
        self.send(const.SCI_SETSELFORE,1,color)
        
    def setup001(self,mainWin=None):
        self.setCaretLineShowAlways(True)
        self.setAutoIndent(True)
        color = QColor('blue')
        color.setAlpha(10)
        self.setCaretLineBack(color)
        self.setMultiCaret(True)
        font = QFont()
        font.setPointSize(12)
        self.setStyleFont(32,font)
        self.extendDefaultStyle()
        self.showNumPanel()
        self.setBackColor(33, QColor('#E6E6E6'))
        
        from heQt.scintilla_p.exraHight import DbFind
        self.setExtraHight(DbFind(self)) 
        
        auto =Autocompleter(self)
        auto.setup001('dogbit')
        self.setAutoCompleter(auto)
        
        
def QcolorToRGB(color):
    r = color.red()
    g = color.green()
    b = color.blue()
    return (r | g << 8 | b << 16)
class c_range(Structure):
    _fields_ = [("start", c_int), 
                 ("end", c_int), 
                 ("style", c_int)]
    

def test():
    #print( editor.getSelection() )
    #editor.addSelection(5,10)
    print(editor.textRange( *editor.getMainSelection() ))
if __name__ == '__main__':
    from cusLexer import Hello
    from autocompleter import Autocompleter
    app = QApplication(sys.argv)
    editor = Scintilla()
    editor.show()
    #editor.setForeColor(33,QColor('red'))
    #editor.setBackColor(33,QColor('yellow'))
    #editor.showNumPanel(True)
    #editor.setLexer(Hello(editor))
    #comp = Autocompleter(editor)
    #comp.setCompKey(Qt.Key_Return)
    auto = Autocompleter(editor)
    editor.setAutoCompleter(auto)
    auto.setup00test()
    
    editor.setText('ririririr')
    editor.setup001()
    act = QPushButton('test')
    act.clicked.connect(test)
    act.show()
    
    sys.exit(app.exec_())