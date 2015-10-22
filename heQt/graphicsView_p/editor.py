"""
暂时没用
"""



from heQt.qteven import *

class Editor:
    def __init__(self, scn, aware=None):
        s(Editor,scn)
        self.scene = scn
        self.aware = aware
        self.lineDrawer = LineDrawer(self)
        self.drawer = None 
        self.drawAct = QAction('画线', self)
        self.drawAct.triggered.connect(self.on_draw_click)
        
    def on_draw_click(self):
        self.drawer = self.lineDrawer   
        
    def actions(self):
        out = []
        if self.drawer:
            out.extend(self.drawer.actions() )
        else:
            out.append(self.drawAct)
        return out
    
    def awarePoint(self):
        if self.aware:
            return self.aware.a
        
    def mousePressEvent(self, event):
        if self.drawer:
            return self.drawer.mousePressEvent(event)
        else:
            return False
    
    def mouseReleaseEvent(self, event):
        if self.drawer:
            return self.drawer.mouseReleaseEvent(event)
        else:
            return False        
        
    def mouseMoveEvent(self, event):
        if self.drawer:
            return self.drawer.mouseMoveEvent(event)
        else:
            return False