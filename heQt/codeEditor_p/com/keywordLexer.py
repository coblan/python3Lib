from ..cusLexerBase import CusLexerBase
class KeyWordLexer(CusLexerBase):
    """
    实现了"关键字"高亮的功能，只需要在子类中：
    1 替换 sytle
    2 重载 initCfg
    
    如果要实现其他复杂高亮：
    1 重载 initCfg
    2 重载 hightText"""
    # style 在子类中替换掉
    style = {0: ["hello"],
             1: ["world", "dog"],}
        
    # 基本不用变，即使在子类中也是
    basePattern = re.compile(r"\w+|!".encode('utf8'))    
    
    @staticmethod
    def getCfgItem():
        it = stdItem("关键字语法器")
        dc = {"CUSLEXER_Df_FORE": ("普通文本前景色", QColor("#000")),
              "CUSLEXER_DF_FONT": ("普通字体",  QFont()),
        }
        ConfigTree.makeItem(it, dc)
        return it
        
    def initCfg(self, cfgDict):
        """设置editor的style，在子类中，重载该函数"""
        
        color = QColor( get_update(cfgDict, "CUSLEXER_Df_FORE", "#000") )
        self.editor.setForeColor(32,  color)
        font = QFont()
        uFont = font.toString()
        font.fromString(get_update(cfgDict, "CUSLEXER_DF_FONT", uFont ) )
        self.editor.setStyleFont(32, font) 
        
        self.editor.extendDefaultStyle()
        
        self.editor.setForeColor(0, QColor(Qt.yellow))
        self.editor.setForeColor(1, QColor(Qt.green))  
        self.editor.setBackColor(33, QColor(Qt.yellow))   
        
    def hightText(self, start, end): 
        text = self.editor.textRange(start, end)
        self.editor.setFormat(start, end, 32)
           
        outStyle = []
        match = True
        end = 0
        while True:
            match = self.basePattern.search(text, end)
            if not match:
                break
            for k, v in self.style.items():
                if match.group().decode("utf8") in v:
                    outStyle.append((start + match.start(), start + match.end(), k))
                    break
            end = match.end()
        self.editor.setFormatList(outStyle)    