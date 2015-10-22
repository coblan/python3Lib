from heQt.qteven import * 
from heQt.codeEditor_p.const import * 
from heQt.codeEditor_p.bridge import Bridge
import re
from heStruct.cls import sub_obj_call

from heQt.codeEditor_p.com.lineManager import LineManager
from ctypes import Structure, c_int
## 常数
SCLEX_CONTAINER = 0
SCLEX_NULL = 1


def QcolorToRGB(color):
    r = color.red()
    g = color.green()
    b = color.blue()
    return (r | g << 8 | b << 16)
class c_range(Structure):
    _fields_ = [("start", c_int), 
                 ("end", c_int), 
                 ("style", c_int)]

class CodeEditorBase(Bridge):
    def __init__(self, *args):
        super().__init__( *args)
        self.send(SCI_SETCODEPAGE, SC_CP_UTF8)
        self.setAutoIndent(True)
        self.send(SCI_SETLEXER, SCLEX_NULL)
        
        self.send(SCI_SETWRAPMODE, SC_WRAP_WORD)
        self.send(SCI_SETWRAPINDENTMODE, SC_WRAPINDENT_SAME)
        self.send(SCI_SETTABWIDTH, 4)
        self.send(SCI_SETMODEVENTMASK, SC_MOD_BEFOREDELETE | SC_MOD_BEFOREINSERT | SC_MOD_INSERTTEXT | SC_MOD_DELETETEXT)
        self.send(SCI_SETMARGINWIDTHN, 1, 0)
        
        self.lineManager = LineManager(self)

    def cursorOnCenter(self, boo = True):
        """是否通过加宽页脚，使文字光标不出现在最下面"""
        if boo:
            self.send(SCI_SETENDATLASTLINE, 0)        # 当输入满一页后，确保光标不必在页的最下面
        else:
            self.send(SCI_SETENDATLASTLINE, 1) 
    def showNumPanel(self, boolv = True, width = 40):
        if boolv:
            self.send(SCI_SETMARGINTYPEN, 0, 1)
            self.send(SCI_SETMARGINWIDTHN, 0, width)
        else:
            self.send(SCI_SETMARGINWIDTHN, 0, 0)
    
    @sub_obj_call
    def onModify(self, type_, pos, length, linesAdd, text, line, foldNow, foldPre):
        "CALLBACK"
        if type_ & SC_MOD_BEFOREDELETE or type_ & SC_MOD_BEFOREINSERT:
            if type_ & SC_MOD_BEFOREDELETE:
                self.beforeDelEvent(pos, length)
            elif type_ & SC_MOD_BEFOREINSERT:
                self.beforeInsertEvent(pos, length)
        else:
            
            if type_ & SC_MOD_INSERTTEXT:
                event = QEvent(QEvent.User)
                event.pos = pos
                event.length = length
                event.handler = self.insertEvent
                #self.insertEvent(pos, length)
                QApplication.postEvent(self, event)
            elif type_ & SC_MOD_DELETETEXT:
                event = QEvent(QEvent.User)
                event.pos = pos
                event.length = length                
                #self.deleteEvent(pos, length)
                event.handler = self.deleteEvent
                QApplication.postEvent(self, event)
            
    
    @sub_obj_call
    def beforeInsertEvent(self, pos, length):
        pass
    @sub_obj_call
    def beforeDelEvent(self, pos, length):
        pass
    @sub_obj_call
    def insertEvent(self, pos, length):
        pass
    @sub_obj_call
    def deleteEvent(self, pos, length):
        pass
    @sub_obj_call
    def beforeKey(self, key, modifier):
        return None
    @sub_obj_call
    def afterKey(self, key, modifier):
        if self.autoIndent:
            self.__autoIndent(key, modifier)
            
    @sub_obj_call
    def doubleClick(self, pos , line):
        pass
    @sub_obj_call
    def mouseClick(self, line, modifier):
        pass
    def customEvent(self, event):
        event.handler( event.pos, event.length)

    
    def grabLine(self, line):
        """返回一个obj是lineManager.GrabLine对象。
        obj.line属性表示行数，该行数是跟随文档变化而刷新的。
        设置回调函数obj.afterLineDel=fun()，可以监视某行被删除
        """
        return self.lineManager.grabLine(line)
    
    def lineFromPos(self, pos):
        return self.send(SCI_LINEFROMPOSITION, pos)
    def posFromLine(self, line):
        return self.send(SCI_POSITIONFROMLINE, line)
    def lineLen(self, line):
        return self.send(SCI_LINELENGTH, line)
    def lineCount(self):
        return self.send(SCI_GETLINECOUNT)
    def lineIndentation(self, line):
        return self.send(SCI_GETLINEINDENTATION, line)
    def currentPos(self):
        return self.send(SCI_GETCURRENTPOS)
    def currentLine(self):
        return self.lineFromPos(self.currentPos())
    def insertText(self, pos, text):
        if isinstance(text, str):
            text = text.encode("utf8")
        self.send(SCI_INSERTTEXT, pos, text)
    def gotoPos(self, pos):
        self.send(SCI_GOTOPOS, pos)
    def setBackColor(self, n, color):
        color = QcolorToRGB(color)
        self.send(SCI_STYLESETBACK, n, color)
    def setForeColor(self, n, color):
        color = QcolorToRGB(color)
        self.send(SCI_STYLESETFORE, n, color)
    def setStyleFont(self, n, font):
        assert isinstance(font, QFont)
        self.send(SCI_STYLESETBOLD, n, 1 if font.bold() else 0)
        self.send(SCI_STYLESETITALIC, n, 1 if font.italic() else 0)
        self.send(SCI_STYLESETWEIGHT, n, font.weight())
        self.send(SCI_STYLESETSIZE, n, font.pointSize())
        self.send(SCI_STYLESETFONT, n, font.family().encode("utf8"))
    def setFormat(self, start, end, n):
        """少量设置高亮，建议使用setFormatList替代"""
        #tmp = self.send(SCI_GETENDSTYLED)
        
        self.send(SCI_STARTSTYLING, start)
        self.send(SCI_SETSTYLING, end - start, n)
        
        #self.send(SCI_STARTSTYLING, tmp)
    def setText(self, string):
        if isinstance(string, str):
            text = string.encode("utf8")
        elif isinstance(string, bytes):
            text = string
        else:
            return
        self.send(SCI_SETTEXT, 0, text)
    def setFormatList(self, ranges, comments = []):
        """ranges是[(start,end,n),]形式的列表
        comments是[0,1,2,3,4]这样的列表，表明comment的标号。它不会影响正常的comment的设置"""
        tmp = self.send(SCI_GETENDSTYLED)
        c_ranges = (c_range * len(ranges))( *ranges)
        c_comments = (c_int * len(comments))( *comments)
        super().setFormatList(c_ranges,  c_comments)
        self.send(SCI_STARTSTYLING, tmp)
    def setReadOnly(self, bool_):
        
        self.send(SCI_SETREADONLY, 1 if bool_ else 0)
        self.send(SCI_SETCARETWIDTH, 0 if bool_ else 1)
    def readOnly(self):
        return self.send(SCI_GETREADONLY)
    def extendDefaultStyle(self):
        """将默认样式传递到所有 style Number上"""
        self.send(SCI_STYLECLEARALL)
    
    def isModified(self):
        return self.send(SCI_GETMODIFY)
    def setSavePoint(self):
        self.send(SCI_SETSAVEPOINT)
        self.send(SCI_EMPTYUNDOBUFFER)
        
    def setAutoIndent(self, boo):
        self.autoIndent = boo
        
    def __autoIndent(self, key, modifiers):
        if  key ==Qt.Key_Return and  modifiers==Qt.NoModifier :
            line = self.currentLine()
            if line >0:
                indent = self.lineIndentation(line-1)
                self.insertText(-1, " " *indent)
                self.gotoPos(self.currentPos()+indent)
    def pointXFromPos(self, pos):
        return self.send(SCI_POINTXFROMPOSITION, 0, pos)
    def pointYFromPos(self, pos):
        return self.send(SCI_POINTYFROMPOSITION, 0, pos)
    def lineHeight(self):
        """所有行都是一样高的"""
        return self.send(SCI_TEXTHEIGHT, 0)
    def getTextLength(self):
        return self.send(SCI_GETTEXTLENGTH)
    def getStyleAt(self, pos):
        """返回某pos处的style number"""
        return self.send(SCI_GETSTYLEAT, pos)
    
    def replaceRange(self, text, pos, len_):
        """@text : utf8"""
        self.send(SCI_BEGINUNDOACTION)
        self.send(SCI_DELETERANGE, pos, len_)
        self.insertText(pos, text)
        self.send(SCI_ENDUNDOACTION)   
    
    def lastOcurrance(self, pattern, pos = None, crossLine = False, flag = 0):
        """寻找上一个发生 Pattern 的地方。注意返回的 match object .group(1) 开始"""
        pattern = (".*(%s).*?$" % pattern).encode("utf8")
        if pos is None:
            pos = self.currentPos()
        line = self.lineFromPos(pos)
        while line >= 0:
            linestart = self.posFromLine(line)
            text = self.textRange(linestart, pos)
            rt = re.match(pattern, text, flag)
            if rt:
                return linestart, rt
            else:
                if not crossLine:
                    return None
                line -= 1
                pos = self.posFromLine(line) + self.lineLen(line)
    def nextOcurrance(self, pattern, pos = None, crossLine = False, flag = 0):
        pattern = ("^.*?(%s)" % pattern).encode("utf8")
        if pos is None:
            pos = self.currentPos()
        line = self.lineFromPos(pos)
        while True:
            text = self.textRange(pos, self.posFromLine(line) + self.lineLen(line))
            rt = re.match(pattern, text, flag)
            if rt:
                return pos, rt
            else:
                if not crossLine:
                    return None
                line += 1
                if line > self.lineCount():
                    return
                else:
                    pos = self.posFromLine(line)
                    

