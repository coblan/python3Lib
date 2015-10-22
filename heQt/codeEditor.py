#
# 本页是为了实现代码编辑器的功能
#CodeEditor:
#    编辑器，具体功能函数在基类里面
#CusLexer:
#    语法解析器
############################

from heQt.codeEditor_p.codeEditorBase import CodeEditorBase
from heQt.codeEditor_p.const import * 
from heQt.codeEditor_p.cusLexerBase import CusLexerBase
from heQt.codeEditor_p.autocompBase import AutocompBase
class CodeEditor(CodeEditorBase):
    """包装scitilla的代码编辑器
    继承关系：
         Bridge<-CodeEditorBase<-CodeEditor
         
    泛化方法：
        send(XXX) :XXX是const下常数，具体含义参看scitilla的文档。

    """
    pass
class CusLexer(CusLexerBase):
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
        1. 设置editor的style （可以在Lexer中来设置），先设置32默认格式，然后调用 send(SCI_STYLECLEARALL)，让所有格式都与默认格式一致。
           然后再来设置其他格式。
        2. 在Lexer中解析的时候设置关键字高亮"""
    pass

class AutoComp(AutocompBase):
    pass
##################################
#
def test():
    s, e = win.nextOcurrance("hello")
    print( s, e )
    print(win.textRange(s, e).decode("utf8"))
if __name__ == "__main__":
    import sys
    #from codeEditor_.cusLexer import CusLexer
    from heQt.qteven import * 
    app = QApplication(sys.argv)
    win = CodeEditor()
    win.showNumPanel(width= 20)
    win.show()
    
    win.setForeColor(32, QColor(Qt.blue))
    win.send(SCI_STYLECLEARALL)
    
    win.setForeColor(0, QColor(Qt.yellow))
    win.setForeColor(1, QColor(Qt.green))  
    win.setBackColor(33, QColor(Qt.yellow))
    font = QFont()
    font.setPointSize(30)
    win.setStyleFont(33, font)
    #win.send(SCI_STYLERESETDEFAULT)
    win.showNumPanel()
    lexer = CusLexer(win)
    


    btn = QPushButton("click")
    btn.clicked.connect(test)
    btn.show()
    
    #for i in range(5):
        #win.setMarginWidthBit(i, 0)
    #win.addNumPanel(5)
    #win.setMarginTypeN(1, 0)
    #win.setMarginWidthBit(1, 1)
    #win.styleSetFore(33, QColor(Qt.blue))
    #win.styleSetBack(33, QColor(Qt.lightGray))
    sys.exit(app.exec_())