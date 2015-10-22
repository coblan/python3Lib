
from heQt.qteven import *
from heQt.scintilla_p.scintilla import Scintilla
import re
class DbFind:
    """双击的时候，查找相同项
    editor.setExtraHight()
    """
    def __init__(self,editor):
        if 0:
            assert isinstance(editor,Scintilla)
        self.editor = editor
        editor.setSelBack(QColor('blue'))
        editor.setSelFore(QColor('white'))
    
    def doubleClick(self, pos, line):
        
        oldrange = self.editor.getMainSelection()
        text = self.editor.textRange(*oldrange)  
        if text:
            self.hight_text(text)
            self.editor.addSelection(*oldrange)
  
    def hight_text(self ,text ):
        pt = b'(?<=\\W)('+text+b')((?=\\W)|$)'
        for i in re.finditer(pt, self.editor.text()):
            self.editor.addSelection(i.start(1),i.end(1))
        
   