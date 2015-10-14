from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from heQt.graphicsView_p.items import *

def dynplug(func):
    '''使用时，类需要有： 
    1.
    self.mapfunc={
            'createLine':{
                'mouseMoveEvent':'',
                'mousePressEvent':'',
            }
        }
    2. self.dynstate = 'createLine'
    '''
    def _func(self, *args, **kw):
        if not hasattr(self,'dynstate'):
            return func(self, *args, **kw)
        dynstate = self.mapfunc.get(self.dynstate, None)
        if dynstate:
            rfunc = dynstate.get(func.__name__,None)
            return rfunc(func, self, *args, **kw)
        else:
            return func(self, *args, **kw)
    return _func


class GraphicsView(QGraphicsView):

    def __init__(self,*args,**kw):
        super().__init__(*args,**kw)
        self.menu = QMenu(self)
        self._msMoveAware = set()
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.TextAntialiasing)
        self.modifier = ''
        self.mapfunc={}
        # 测试划线
        self.dynstate = '' #'createLine'
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        AwareItem.rigisterView(self)
        LineStrip.rigisterView(self)
        
    def registFreeMSmoveAware(self,cls):
        self._msMoveAware.add(cls)
        
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
        
    @dynplug
    def mousePressEvent(self,event):
        return super().mousePressEvent(event)
    
    @dynplug
    def mouseReleaseEvent(self,event):
        return super().mouseReleaseEvent(event)
    
    @dynplug
    def mouseMoveEvent(self,event):
        if event.buttons() == Qt.NoButton:
            if isinstance( self.itemAt(event.pos()),tuple(self._msMoveAware)):
                pos = self.mapToScene(event.pos())
                self.itemAt(event.pos()).MSFreeMove(pos,self)
            else:
                self.setCursor(Qt.ArrowCursor)
        return super().mouseMoveEvent(event)
    
    @dynplug
    def proxyplug1(self):
        pass
    
    def contextMenuEvent(self,event):
        self.under_ms_item = self.itemAt(event.pos())
        self.menu.clear()
        if hasattr(self.under_ms_item,'actions'):
            self.menu.addActions(self.under_ms_item.actions( posScen=self.mapToScene(event.pos())))
        self.menu.addActions(self.actions())
        self.menu.exec_(self.viewport().mapToGlobal(event.pos()))
    
    @dynplug
    def actions(self):
        return super().actions()
           
class GView1(GraphicsView):
    def __init__(self,parent=None):
        super().__init__(parent)

    def dev(self):
        self.setMouseTracking(True)
        self.setScene(MyScent())
        self.setDragMode(QGraphicsView.RubberBandDrag)
        #for i in range(30):
            #item = TryItem()
            #item.setRect(0,0, 100, 100)
            #self.scene().addItem( item )
        #self.scene().addItem(LineStrip([QPoint(0,0),QPoint(100,100),QPoint(300,0)]))
        self.scene().setSceneRect(0,0,500,500)
        print(self.scene().sceneRect())
    
    def actions(self):
        out =[]
        if not hasattr(self,'has_action'):
            self.act1 = QAction('画线',self)
            self.act2 = QAction('设置', self)
            self.act3 = QAction('拖动',self)
            self.act1.triggered.connect(self.on_act1)
            self.act2.triggered.connect(self.on_act2)
            self.act3.triggered.connect(self.on_act3)
        if self.dynstate !='createLine':
            out.append(self.act1)
        out.append(self.act2)
        out.append(self.act3)
        out.extend(super().actions())
        return out
            
    def on_act1(self):
        self.dynstate = 'createLine'
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
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        
class MyScent(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grabber = ''
        self.setSceneRect(-500,-500,1000,1000)
    def mouseGrabberItem(self):
        print('iiii')
        if self.grabber:
            return self.grabber
        else:
            return super().mouseGrabberItem()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    mainWin = QMainWindow()
    win = GView1(mainWin)
    #LineStrip.rigisterView(win)
    #AwareItem.rigisterView(win)
    
    mainWin.setCentralWidget(win)
    mainWin.show()
    
    win.dev()
    sys.exit(app.exec_())