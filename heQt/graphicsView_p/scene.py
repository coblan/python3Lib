from heQt.qteven import *
from heStruct.pyeven import *


class Scene(QGraphicsScene):
    """
    Manager功能
    mouserMoveEvent()写了aware
    
    使用时：
    1. setAware(Aware(self)) ;
    2. appendDrawer()
    
    """
    def __init__(self, parent=None):
        s(Scene, parent)
        #self.setSceneRect(-500,-500,1000,1000)
        
        self.aware = None
        self.drawer = None
        self.drawerPool =[]
        #self.lineDrawer = LineDrawer(self, self.aware)
            
    def appendDrawer(self,drawer):
        self.drawerPool.append(drawer)
        drawer.setAware(self.aware)
        
    def setAware(self,aware):
        self.aware = aware
        
    def clear(self):
        cls=None
        if self.aware:
            cls = type(self.aware)
        s(Scene)
        if cls:
            self.aware = cls(self)
    
    def actions(self):
        if self.drawer:
            return self.drawer.actions()
        else:
            ls =[]
            for i in self.drawerPool:
                ls.extend(i.actions())
            return ls
        
    def awarePoint(self):
        if self.aware:
            return self.aware.awarePoint()
    
    def setAwarePoint(self, point):
        if self.aware:
            self.aware.setAwarePoint(point)
        
    def mouseMoveEvent(self, event):
        if self.aware:
            self.aware.mouseMoveEvent(event)

        if self.drawer and self.drawer.mouseMoveEvent(event):
            return
        return s(Scene,event)

    def mousePressEvent(self,event):
        if self.drawer and not self.drawer.mousePressEvent(event):
            return
        return s(Scene,event)

    def mouseReleaseEvent(self,event):
        if self.drawer and self.drawer.mouseReleaseEvent(event):
            return
        return s(Scene, event)