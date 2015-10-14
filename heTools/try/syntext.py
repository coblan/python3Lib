from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import re
class Editor(QPlainTextEdit):
    #def __init__(self, parent=None):
        #super().__init__(parent)
        #self.input = q
    def mouseDoubleClickEvent(self,event):
        rt = super().mouseDoubleClickEvent(event)
        text = self.textCursor().selectedText()  
        if text:
            self.hight_text(text)
        return rt
    
    def hight_text(self ,text ):
        old = self.textCursor()
        old_pos = self.verticalScrollBar().value()
        new =QTextCursor(self.document())
        new.movePosition(QTextCursor.Start)
        self.setTextCursor(new)            
        extraSelections= []
        while self.find(text,QTextDocument.FindWholeWords):
            extra = QTextEdit.ExtraSelection()
            extra.cursor = self.textCursor()
            extra.format.setBackground(QColor('#CDCD00'));
            extraSelections.append(extra)
    
        self.setExtraSelections(extraSelections)
        self.setTextCursor(old)
        self.verticalScrollBar().setValue(old_pos)  
        
    def mousePressEvent(self,event):
        extra = self.extraSelections()
        if extra:
            self.setExtraSelections([])

        return super().mouseReleaseEvent(event)
    
    def keyPressEvent(self,event):
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_F:
            text,ok = QInputDialog.getText(self,'搜索','文字')
            if ok and text:
                self.hight_text(text)
        else:
            return super().keyPressEvent(event)
    
class SynModel(QSyntaxHighlighter):
    kw = re.compile('class|def\s+')
    model =re.compile('models.')
    key = re.compile('ForeignKey|OneToOneField|ManyToManyField')
    comment = re.compile ('^\s*#.*$')
    
    def highlightBlock(self,text):
        charf = QTextCharFormat()
        charf.setFontWeight(QFont.Bold)
        charf.setForeground(Qt.blue)
        
        purp = QTextCharFormat()
        purp.setForeground(QColor('#FAAC58'))
        
        bg_yellow = QTextCharFormat()
        bg_yellow.setBackground(QColor('#F7FE2E'))
        
        green = QTextCharFormat()
        green.setForeground(QColor('#58FA58'))
        
        for mt in self.kw.finditer(text):
            self.setFormat(mt.start(),mt.end()-mt.start(),charf)
            
        for mt in self.model.finditer(text):
            self.setFormat(mt.start(),mt.end()-mt.start(),purp)  
        
        for mt in self.key.finditer(text):
            self.setFormat(mt.start(),mt.end()-mt.start(),bg_yellow)          
            
        for mt in self.comment.finditer(text):
            self.setFormat(mt.start(),mt.end()-mt.start(),green)              
            
        