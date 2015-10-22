from heQt.qteven import *
from heQt.scintilla import *
import re
from heStruct.pyeven import *

class Editor(Scintilla):
    def __init__(self, parent=None):
        s(Editor,parent)
        
        self.setup001()
        
        self.setLexer(Lexer(self))
        



class Lexer(CusLexer):
    kw = re.compile(b'class|def\s+')
    model =re.compile(b'models.')
    key = re.compile(b'ForeignKey|OneToOneField|ManyToManyField')
    comment = re.compile (b'^\s*#.*$',re.M ) 
    
    def __init__(self, editor):
        s(Lexer,editor)
        self.colors={
            'kw':1,
            'model':2,
            'key':3,
            'comment':4
        }

        self.editor.setForeColor(1, QColor('blue'))
        font =QFont(self.editor.getStyleFont())
        font.setBold(True)
        font.setItalic(True)
        self.editor.setStyleFont(1, font)
        
        self.editor.setForeColor(2,QColor('red'))
        self.editor.setBackColor(3,QColor('yellow'))
        self.editor.setForeColor(4,QColor('green'))
        

        
    def hightText(self, start, end):
        self.editor.setFormat(start, end, 32)
        text = self.editor.textRange(start, end)
        out = []
        for i in Lexer.comment.finditer(text):
            out.append( ( start+i.start(),start+i.end(),self.colors['comment']) )
        for i in Lexer.kw.finditer( text):
            out.append( ( start+i.start(),start+i.end(),self.colors['kw']) )
        for i in Lexer.key.finditer( text):
            out.append( ( start+i.start(),start+i.end(),self.colors['key']) )        

        self.editor.setFormatList(out, [self.colors['comment']]) 
        
        
class AutoComp(Autocompleter):
    pass

    
            
            
        