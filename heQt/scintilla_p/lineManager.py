
from heStruct.cls import add_sub_obj


class GrabLine(object):
    "抓行对象//self.afterLineDel()  # CALLBACK 行被删除的时候调用"
    def __init__(self, line, manager):
        self.line = line
        self.manager = manager
        self.afterLineDel = None
    def doDel(self):
        if self.afterLineDel:
            self.afterLineDel()  # CALLBACK 行被删除的时候调用
        self.uninstall()
    def uninstall(self):         # 当不追踪该行时，记得调用该函数
        if self in self.manager.grabedLines:
            self.manager.grabedLines.remove(self)
            self.line = -1       # 防止误用
    def __eq__(self, other):
        return self is other
    
    
class LineManager(object):
    """管理CodeEditor的行
    功能:
    
    *. self.grabLine(line) ,抓住某行，返回GrabLine对象，如果要Listion 行删除事件，需要为返回的GrabLine对象添加afterLineDel()
    *. 自动调整 grabLine抓住的行号。
    """
    def __init__(self, editor):
        self.editor = editor
        add_sub_obj(editor, self)
        self.grabedLines = []
    
    def grabLine(self, line):
        """抓住第line行，返回GrabLine对象"""
        wrap = GrabLine(line, self)
        self.grabedLines.append(wrap)
        return wrap    
    
    def onModify(self, type_, pos, length, linesAdd, text, line, foldNow, foldPre):
        if linesAdd != 0:
            self._lineNumChanged(pos, linesAdd)
            
    def _lineNumChanged(self, pos, lineAdd):
        """CALLBACK ,当行数发生变化时，利用该函数调整以前抓住的行"""
        line = self.editor.lineFromPos(pos)
        if lineAdd > 0:
            for itm in self.grabedLines:
                num = itm.line
                if num > line:
                    itm.line = num + lineAdd         
        elif lineAdd < 0:
            ls = []
            for itm in self.grabedLines:
                num = itm.line
                if line < num <= line + abs(lineAdd):
                    ls.append(itm)
                elif line < num:
                    itm.line = num + lineAdd
    
            for itm in ls:
                itm.doDel()   