from qt_.qtEven import * 
from qt_.view_.codeEditor_.utiliz.cusLexer import CusLexer, Style
import re
class TPLexer1(CusLexer):
    """功能：高亮关键字，可以自定义hightEvent
启动步骤:
    1. 调用self.addStyles() ,来覆盖styles设定
    2. 重写 CLS.keyWords 属性。注意和styles中项的名字要一致。如 [3]
    3. 可以在子类中重写hightEvent ,注意如果要继续支持keyword高亮，必须调用self.hightKeyWord,并且传递其返回的结构。如[1]
    4. 在宿主editor中，调用editor.addFunction(TPLexer1()) 。如 [2]

    """
    # [3] 这里是关键字的例子，屏蔽掉，免得对子类造成干扰。可以按照样子在子类中定义关键字。 see also [4]
    #keyWords = {"hight1": ("hello", "world"),  
                #"hight2": ("fuck", "wawa"),}
    keyWords = {}
    
    basePattern = re.compile(r"\w+|!".encode('utf8'))
    def __init__(self, *args):
        super().__init__( *args)
        self.addStyles( {"comment": Style(0, fore= QColor(Qt.gray)), }) 
                          #"hight1": Style(1, fore= QColor(Qt.red)),
                          #"hight2": Style(2, fore = QColor(Qt.blue)),} )  # [4]

    def hightEvent(self, bStr, pos):
        """高亮，以下是样例，添加了 #开头的评论的高亮功能"""
        out = []
        out.extend( self.hightKeyWord(bStr, pos) )  # [1] 如果要继续支持keyword高亮，需要传递self.hightKeyWord的返回值
        
        for mt in re.finditer(r"^[ \t]*#.*$".encode("utf8"), bStr, re.MULTILINE):
            out.append((mt.start() + pos, mt.end() + pos, self.num("comment")) )
        return out
    def hightKeyWord(self, bStr, pos):
        if not self.keyWords:
            return []
        outStyle = []
        match = True
        end = 0
        while True:
            match = self.basePattern.search(bStr, end)
            if not match:
                break
            for k, v in self.keyWords.items():
                if match.group().decode("utf8") in v:
                    outStyle.append((pos + match.start(), pos + match.end(), self.num(k)))
                    break
            end = match.end()   
        return outStyle

   
if __name__ == "__main__":
    import sys
    from qt_.view_.codeEditor_.codeEditor import CodeEditor
    app = QApplication(sys.argv)
    win = CodeEditor()
    win.addFunction(TPLexer1())  # [2]
    win.show()
    sys.exit(app.exec_())