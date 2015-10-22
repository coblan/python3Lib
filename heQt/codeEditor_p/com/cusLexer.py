######################################################
"""
过期了。。。。。。。

实现自定义Lexer的基础组件。
CusLexer 是自定义Lexer基类
Style 用于描述每项style的数据结构
"""
######################################################

from qt_.qtEven import * 
from struct_.design_ import add_sub_obj
if 0:
    from .. codeEditor import CodeEditor
from ..const import * 
import re
class Style(object):
    """每项样式，在cuslexer的styles属性中使用"""
    def __init__(self, num, font = None, fore = None, back = None):
        self.num = num
        self.font = font
        self.fore = fore
        self.back = back
    def apply(self, editor):
        """应用到editor"""
        if 0:
            assert isinstance(editor, CodeEditor)    
        if self.fore:
            editor.setForeColor(self.num, self.fore)
        if self.back:
            editor.setBackColor(self.num, self.back)
        if self.font:
            editor.setStyleFont(self.num, self.font)

class CusLexer(QObject):
    """Lexer的基类
    重要函数或功能：
    *. styles 类属性，用于记录styles，注意：每项都是 Style()
    
    *. 重写hightEvent() ，用于刷新文字
    *. self.num("name") ,用于从名字name返回相应的number号
    *. self.hightLine(Line),刷新某行 
    
    其他能力：
    能够自动刷新最后一行，函数为：_checkAndUpdateEndLine，其将在hightNotify()中自动被调用
    
    利用editor的add_sub_obj结构，自动调用insertEvent。
    
    """
    def __init__(self, *args):
        super().__init__( *args)
        self.editor = None
        self.styles = {"default": Style(32)}
        
    def addStyles(self, styles):
        self.styles.update(styles)
        self.__updateEditorStyle()
         
    def install(self, editor):
        if 0:
            assert isinstance(editor, CodeEditor)
        self.editor = editor
        add_sub_obj(editor, self)
        self.__updateEditorStyle()
           
    def num(self, name):
        return self.styles[name].num

    def hightEvent(self, bStr, pos):
        """被hightNotify调用的回调函数。你需要自定义该函数。不要直接调用该函数。
        bStr : utf8格式的文字，它们需要style
        返回格式：[(start,end,num),] """
        return []
    def hightNotify(self, pos, length ):
        """高亮pos到length的文字。不要直接调用hightEvent，因为hightNotify有很多额外的完善代码"""
        text = self.editor.textRange(pos, pos + length)
        self.editor.setFormat(pos, pos + length, 32)
        
        # 就是这一行，返回自定义函数的结果
        outStyle = self.hightEvent(text, pos)

        self.editor.setFormatList(outStyle)
        self._checkAndUpdateEndLine(pos )
        
    def hightLine(self, line):
        pos = self.editor.posFromLine(line)
        length = self.editor.lineLen(line)
        self.hightNotify(pos, length)
##################################################
# 以下是被 editor回调的函数
    def insertEvent(self, pos, length):
        line = self.editor.lineFromPos(pos)
        start = self.editor.posFromLine( line )
        endLine = self.editor.lineFromPos(pos + length)
        end = self.editor.posFromLine(endLine) + self.editor.lineLen(endLine)        
        self.hightNotify(start, end - start)
    
    def deleteEvent(self,pos, length):
        line = self.editor.lineFromPos(pos)
        self.hightLine(line)
####################################################
    def _checkAndUpdateEndLine(self, pos):
        line = self.editor.lineFromPos(pos)
        endLine = self.editor.lineCount() - 1
        if line != endLine:
            self.hightLine(endLine)  

    def __updateEditorStyle(self):
        if not self.editor:
            return
        self.styles["default"].apply(self.editor)
        self.editor.send(SCI_STYLERESETDEFAULT) 
        for k, v in self.styles.items():
            if k != "default":
                v.apply(self.editor)  

        
                