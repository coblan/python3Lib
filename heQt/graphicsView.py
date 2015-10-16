from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from heQt.graphicsView_p.items import *
from heStruct.cls import dynplug

class GraphicsView(QGraphicsView):

    def __init__(self,*args,**kw):
        super().__init__(*args,**kw)
        self.menu = QMenu(self)
        #self._msMoveAware = set()
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.TextAntialiasing)
        self.modifier = ''
        self.mapfunc={}
        
        
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        
        
    def wheelEvent(self,event):
        if self.modifier == Qt.ControlModifier:
            factor = event.angleDelta().y() / 130
            if factor < 0:
                factor = 1/(-factor)
            self.scale(factor, factor)  
        else:
            return super().wheelEvent(event)
        
    def keyPressEvent(self, event):
        self.modifier =  event.modifiers() 
        return super().keyPressEvent(event)
    
    def keyReleaseEvent(self,event):
        self.modifier = event.modifiers() 
        super().keyReleaseEvent(event)
        
 
    
    def contextMenuEvent(self,event):
        self.under_ms_item = self.itemAt(event.pos())
        self.menu.clear()
        if hasattr(self.under_ms_item,'actions'):
            self.menu.addActions(self.under_ms_item.actions( posScen=self.mapToScene(event.pos())))
        self.menu.addActions(self.actions())
        self.menu.exec_(self.viewport().mapToGlobal(event.pos()))
    
    #@dynplug('manager')
    def actions(self):
        return s(GraphicsView)

  
class Manager(QObject):
    def __init__(self, scn):
        s(Manager,scn)
        self.scene = scn
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
    
    #@dynplug('drawer')
    def mousePressEvent(self, event):
        if self.drawer:
            return self.drawer.mousePressEvent(event)
        else:
            return False
    
    #@dynplug('drawer')
    def mouseReleaseEvent(self, event):
        if self.drawer:
            return self.drawer.mouseReleaseEvent(event)
        else:
            return False        
    
    #@dynplug('drawer')
    def mouseMoveEvent(self, event):
        if self.drawer:
            return self.drawer.mouseMoveEvent(event)
        else:
            return False
        

import pickle           
class GView1(GraphicsView):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.act2 = QAction('设置', self)
        self.act3 = QAction('拖动',self)

        self.act2.triggered.connect(self.on_act2)
        self.act3.triggered.connect(self.on_act3)
        
    def dev(self):
        #self.setMouseTracking(True)
        self.setScene(Scene())
        self.setDragMode(QGraphicsView.RubberBandDrag)
        for i in range(30):
            item = TryItem()
            item.setRect(0,0, 100, 100)
            self.scene().addItem( item )
        #self.scene().addItem(LineStrip([QPoint(0,0),QPoint(100,100),QPoint(300,0)]))
        self.scene().setSceneRect(0,0,500,500)
        print(self.scene().sceneRect())
        self.load()
        
    def save(self):
        lines = []
        for i in self.scene().items():
            if isinstance(i,LineStrip):
                lines.append(i)
        with open('d:/try/savetest','wb') as f:
            pickle.dump(lines,f)
    
    def load(self):
        lines =[]
        try:
            with open('d:/try/savetest','rb') as f:
                lines = pickle.load(f)
        except Exception :
            pass
        for i in lines:
            self.scene().addItem(i)
            
    def actions(self):
        out =[]

        #if self.scene().state != 'create':
            #out.append(self.act1)
        out.append(self.act2)
        out.append(self.act3)
        out.extend(s(GView1))
        out.extend(self.scene().actions())

        return out
            

        
    def on_act2(self):
        text, ok = QInputDialog.getText(None,'get','长X宽')
        w, l = (int(i) for i in text.split(','))
        px,py =  -w/2 , -l/2
        rect = QRectF(px, py, w, l)
        print(rect)
        self.scene().setSceneRect(rect)
        
        if hasattr(self,'snRect'):
            self.scene().removeItem(self.snRct)
        self.snRct = QGraphicsRectItem()
        
    #def paint(self,painter,option, widget=None):
        rect = self.scene().sceneRect()
        #rect = self.mapFromScene(rect).boundingRect()
        #painter.drawRect(rect)
        self.snRct.setRect(rect)
        self.scene().addItem(self.snRct)
        self.snRct.setZValue(-100)
        #self.setSceneRect(self.scene().sceneRect())
        #print(self.scene().sceneRect())
        
    def on_act3(self):
        #self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.save()
        
    #def paintEvent(self, event):
        #painter = QPainter(self.viewport())
        #painter.drawEllipse(0,0, 100,100)
        #print('ok')
        
        
class Scene(QGraphicsScene):
    """
    Manager
    mouserMoveEvent()写了aware
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSceneRect(-500,-500,1000,1000)
        
        self.aware = CollideItem()
        self.addItem(self.aware)
        #self.awarePath = QPainterPath()
        #self.awarePath.addEllipse(0,0,10,10)
        self.awarePoint = None
        self.awareItem = None

        self.manager = Manager(self)
        
    def clear(self):
        s(Scene)
        self.aware = CollideItem()
        
    def mouseMoveEvent(self, event):
        scnPos=event.scenePos()
        self.aware.setPos(scnPos)
        grab = self.mouseGrabberItem()
        
        self.awarePoint = None
        
        awareitem = None
        for i in self.collidingItems(self.aware):
            if i == grab :
                continue
            elif hasattr(i,'aware'):
                awareitem = i
                break
            
        if awareitem != None:
            if self.awareItem != awareitem and self.awareItem !=None:
                self.awareItem.aware(False,scnPos)
            self.awareItem = awareitem
            self.awareItem.aware(True, scnPos)
        else:
            if self.awareItem !=None:
                self.awareItem.aware(False, scnPos)
                self.awareItem = None
            
        if not self.manager.mouseMoveEvent(event):
            return s(Scene,event)
    
    #def event(self, event):
    #@dynplug('manager')
    def mousePressEvent(self,event):
        if not self.manager.mousePressEvent(event):
            return super().mousePressEvent(event)

    #@dynplug('manager')
    def mouseReleaseEvent(self,event):
        if not self.manager.mouseReleaseEvent(event):
            return super().mouseReleaseEvent(event)

    def actions(self):
        return self.manager.actions()
        

class CollideItem(QGraphicsItem):
    def __init__(self, parent=None):
        super().__init__(parent)
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
    
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    mainWin = QMainWindow()
    win = GView1(mainWin)

    
    mainWin.setCentralWidget(win)
    mainWin.show()
    
    win.dev()
    sys.exit(app.exec_())