from heQt.qteven import * 
from heStruct.cls import add_sub_obj
if 0:
    from scintilla import Scintilla
import re
import sys
#from qt_.model_.item import stdItem
#from qt_.widget.configTree import ConfigTree
#from struct_.objs import get_update

class CusLexer(QObject):
    """Lexer基类，构造函数直接 将lexer插在editor上
    
    重载 hightText 函数
    """     
    def __init__(self, editor):
        """可以在构造函数中设置各种样式。最好从1开始。
        self.editor.setForeColor(1,QColor('red'))
        """
        super().__init__(editor)
        self.editor = editor
        if 0: 
            assert isinstance(editor, Scintilla)   
        #add_sub_obj(editor, self)  
    

    def hightText(self, start, end):
        """在子类中，这里面写功能函数
        样例：
        text = self.editor.textRange(start, end)
        self.editor.setFormat(start, end, 32)
        
        match = dosome_math(text,pattern)
        ls=[(start + match.start(), start + match.end()，k)]   # k是style号

        self.editor.setFormatList(ls)
        """
        pass
    
    def insertEvent(self, pos, length):
        """总的促发高亮的 回调函数
        判断一下是否是最后一行，如果不是，还要单独刷新一下最后一行
        """
        self.hightRange(pos, length)
    
    def deleteEvent(self,pos, length):
        line = self.editor.lineFromPos(pos)
        self.hightLine(line)
        
    def hightRange(self, pos, length):
        line = self.editor.lineFromPos(pos)
        start = self.editor.posFromLine( line )
        endLine = self.editor.lineFromPos(pos + length)
        end = self.editor.posFromLine(endLine) + self.editor.lineLen(endLine) 
        
        self.hightText(start, end)
        
        # 由于最后一个字符高亮问题，所以每次都重新刷新一下最后一行
        #self.__checkAndUpdateEndLine(pos )
        self.bugLastWord()

    def hightLine(self, line):
        pos = self.editor.posFromLine(line)
        length = self.editor.lineLen(line)
        self.hightRange(pos, length)
        
    #def __checkAndUpdateEndLine(self, pos):

        #line = self.editor.lineFromPos(pos)
        #endLine = self.editor.lineCount() - 1
        #if line != endLine:
            #self.hightLine(endLine)     
    
    def bugLastWord(self):
        end = self.editor.getTextLength() - 1
        number = self.editor.getStyleAt(end)
        #if number == 0:
            #before_number = self.editor.getStyleAt(end - 1)
        #self.endNumber = number
        self.editor.setFormat(end, end + 1, number)
        #else:
            
        #print(number)
        #print(self.editor.textRange(end, end + 1))        



class Hello(CusLexer):
    def __init__(self, editor):
        super(Hello,self).__init__(editor)
        self.editor.setForeColor(1,QColor('red'))
    
    
    def hightText(self, start, end):
        self.editor.setFormat(start, end, 32)
        text = self.editor.textRange(start, end)
        out = []
        for i in re.finditer(b'hello', text):
            out.append( ( start+i.start(),start+i.end(),1) )
        self.editor.setFormatList(out)