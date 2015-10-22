#! -*- encoding:utf8 -*-
from __future__ import unicode_literals
from heQt.qteven import *
from heQt.graphicsView_p.items import *
from heStruct.cls import dynplug
from heQt.graphicsView_p.aware import Aware
from heQt.graphicsView_p.scene import Scene

class GraphicsView(QGraphicsView):

    def __init__(self,*args,**kw):
        super().__init__(*args,**kw)
        self.menu = QMenu(self)
        #self._msMoveAware = set()
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.TextAntialiasing)
        self.modifier = ''
        #self.mapfunc={}
        
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        
    def wheelEvent(self,event):
        if self.modifier == Qt.ControlModifier:
            factor = event.angleDelta().y() / 130
            if factor < 0:
                factor = 1/(-factor)
            self.scale(factor, factor)  
        else:
            return s(GraphicsView,event)
        
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
    

    def actions(self):
        return s(GraphicsView)
    
    def setupMainwin(self,mainWin):
        if 0:
            assert isinstance(mainWin,QMainWindow)
        act = QAction('大小',mainWin)
        act.triggered.connect(self._on_size_click)
        toolbar = QToolBar('graphics',mainWin)
        toolbar.addAction(act)
        mainWin.addToolBar(toolbar)
        
    def _on_size_click(self):
        oldrect = self.scene().sceneRect()
        oldtext='%s,%s,%s,%s'%(oldrect.left(),oldrect.top(),oldrect.width(),oldrect.height())
        text, ok = QInputDialog.getText(None,'设置页面大小','格式(-100,-100,200,200)(左上角x，左上角y，宽，高)',text=oldtext)
        if text:
            ls = text.split(',')
            dog =[float(i) for i in ls]
            #rect = QRectF(*dog)
            self.scene().setSceneRect(*dog)



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
        scene = Scene()
        aware = Aware(scene)
        scene.setAware(aware)
        scene.appendDrawer(LineDrawer(scene,aware))
        self.setScene(scene)
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
        

    
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    mainWin = QMainWindow()
    win = GView1(mainWin)

    mainWin.setCentralWidget(win)
    mainWin.show()
    win.setupMainwin(mainWin)
    win.dev()
    sys.exit(app.exec_())