from heQt.qteven import *
from heStruct.pyeven import *

class Aware:
    def __init__(self,scene):
        s(Aware)
        
        self._awarePoint = None
        self.awareItem = None 
        
        if 0:
            assert isinstance(scene, QGraphicsScene)
        self.scene = scene
        self.detector = CollideItem()
        scene.addItem(self.detector)
    
    def awarePoint(self):
        return self._awarePoint
    def setAwarePoint(self,point):
        self._awarePoint = point
        
    def mouseMoveEvent(self, event):
        scnPos=event.scenePos()
        self.detector.setPos(scnPos)
        grab = self.scene.mouseGrabberItem()
    
        self._awarePoint = None
    
        awareitem = None
        for i in self.scene.collidingItems(self.detector):
            if i == grab :
                continue
            elif hasattr(i,'aware'):
                awareitem = i
                break
    
        if awareitem != None:
            if self.awareItem != awareitem and self.awareItem !=None:
                self.awareItem.aware(False,scnPos)
            self.awareItem = awareitem
            self._awarePoint = self.awareItem.aware(True, scnPos)
        else:
            if self.awareItem !=None:
                self.awareItem.aware(False, scnPos)
                self.awareItem = None        


class CollideItem(QGraphicsItem):
    def __init__(self, parent=None):
        s(CollideItem, parent)
        self.radius = 10
        
    def paint(self, painter, option, widget=None):
        pass
        #painter.drawEllipse(0,0,self.radius,self.radius)
        
    def boundingRect(self):
        return QRectF(0,0,self.radius*2,self.radius*2)
    
    def shape(self):
        path = QPainterPath()
        path.addEllipse(-self.radius, -self.radius, self.radius*2, self.radius*2)
        return path