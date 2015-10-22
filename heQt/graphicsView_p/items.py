from heQt.qteven import *
from heStruct.pyeven import *
    

class ControlRect(QGraphicsItem):
    """
    控制方框。
    """
    def __init__(self, item ,parentItem=None):
        s(ControlRect, parentItem)
        self.controllerRadius = 6
        self.margin = self.controllerRadius
        #self.item = item
        self.lastPos = None
        self.msState = -1
        
        self.setParentItem(item)

        self.rect = item.boundingRect()
        
        # 本来不需要 movable的，但是为了和下面的item抢事件，所以设置了个Movable
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setAcceptHoverEvents(True)

    def resize(self,qrect):

        self.prepareGeometryChange()
        self.rect = qrect
        self.setSize(qrect)
        #self.update()

    def setSize(self, qrect = None):
        p = self.parentItem()
        if p and hasattr(p,'setSize'):
            p.setSize(qrect)
                
    def boundingRect(self):   
        rect = self.rect.adjusted(-self.margin,-self.margin,self.margin,self.margin)
        return rect
    
    def _controller(self):
        tl,tr,bl,br = self.rect.topLeft(),self.rect.topRight(),self.rect.bottomLeft(),self.rect.bottomRight()
        tm = QPointF(tl.x()+(tr.x()-tl.x())/2,tl.y())
        ml, mr = QPointF(bl.x(),tl.y()+(bl.y()-tl.y())/2), QPointF(br.x(),tr.y()+(br.y()-tr.y())/2)
        bm = QPointF(bl.x()+(br.x()-bl.x())/2, bl.y())
        ls = [tl,tm,tr,ml,mr,bl,bm,br]
        out = []
        for i in ls:
            out.append( QRectF(i.x()-self.controllerRadius,i.y()-self.controllerRadius,self.controllerRadius*2,self.controllerRadius*2) )
        return out
    
    def sceneEvent(self,event):
        if self.msState == -1 :
            event.ignore()
        return super().sceneEvent(event)
        
    def mouseMoveEvent(self,event):
        if self.msState ==-1:
            # 这里不会被运行到，因为在ScenEvent里面已经将时间路由到底层item去了
            return super().mouseMoveEvent(event)
        elif self.lastPos !=None:
            rect = self.rect
            if self.scene().awarePoint() != None:
                p = self.mapFromScene(self.scene().awarePoint())
            else:
                p = event.pos()
            dx ,dy =p.x()-self.lastPos.x() , p.y()-self.lastPos.y() 
            if self.msState == 0:
                if dy > 0 and self.rect.height() < 10:
                    dy = 0
                if dx > 0 and self.rect.width() < 10:
                    dx = 0
                rect = self.rect.adjusted(dx,dy,0,0)
            elif self.msState == 1:
                if dy > 0 and self.rect.height()<10:
                    dy =0
                rect = self.rect.adjusted(0,dy,0,0)
            elif self.msState == 2:
                if dx < 0 and self.rect.width() < 10:
                    dx = 0
                if dy > 0 and self.rect.height()<10:
                    dy = 0 
                rect = self.rect.adjusted(0,dy,dx,0)
            elif self.msState == 3:
                if dx >0 and self.rect.width() <10:
                    dx = 0
                rect = self.rect.adjusted(dx,0,0,0)
            elif self.msState == 4:
                if dx <0 and self.rect.width() <10:
                    dx = 0
                rect = self.rect.adjusted(0,0,dx,0)
            elif self.msState ==5:
                if dx>0 and self.rect.width()<10:
                    dx =0
                if dy <0 and self.rect.height()<10:
                    dy = 0
                rect = self.rect.adjusted(dx,0,0,dy)
            elif self.msState ==6:
                if dy <0 and self.rect.height()<10:
                    dy =0
                rect =self.rect.adjusted(0,0,0,dy)
            elif self.msState == 7:
                if dx <0 and self.rect.width()<10:
                    dx =0
                if dy <0 and self.rect.height() <10:
                    dy =0
                rect =self.rect.adjusted(0,0,dx,dy)
            
            self.lastPos += QPointF(dx,dy) 
            self.resize(rect)
            
    def mousePressEvent(self,event):
        self.lastPos = event.pos()
        return super().mousePressEvent(event)
    
    def mouseReleaseEvent(self,event):
        self.lastPos = None
        return super().mouseReleaseEvent(event)
    
    def paint(self, painter, option, widget=None):
        painter.drawRect(self.rect)
        painter.drawRects(self._controller())
        #for i in self._controller():
            #painter.fillRect(i,QColor('black') ) 
            
    def hoverEnterEvent(self,event):
        view = event.widget()
        view.setCursor(Qt.SizeAllCursor)
        
    def hoverLeaveEvent(self,event):
        view = event.widget()
        view.setCursor(Qt.ArrowCursor)
        
    def hoverMoveEvent(self,event):
        view = event.widget()
        pos = event.pos()
        rects = self._controller()
        index = -1
        for i in rects:
            index+=1
            if i.contains(pos):
                break
            elif index ==7:
                index =-1
        self.msState = index
        if index in  [0,7]:
            view.setCursor(Qt.SizeFDiagCursor)
        elif index in [1,6]:
            view.setCursor(Qt.SizeVerCursor)
        elif index in [2,5]:
            view.setCursor(Qt.SizeBDiagCursor)
        elif index in [3,4]:
            view.setCursor(Qt.SizeHorCursor)
        else:
            view.setCursor(Qt.SizeAllCursor)


class LineStrip(QGraphicsItem):
    def __init__(self, points=None, parent=None):
        s(LineStrip, parent)
        self.crt_point = None
        self.radius = 6
        self.grabRadius = 10
        #for p in points:
            #i = PointItem(self)
            #i.setPos(p)
        self.points = points
        
        #self.msPoint = None
        self.awarePoint = None
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setAcceptHoverEvents(True)
        
        self.act1 = QAction('插入点', None)
        self.act2 = QAction('删除当前点', None)
        self.act1.triggered.connect(self.on_insert_act)
        self.act2.triggered.connect(self.on_rm_act)
        
    def setPoints(self,points):
        self.points = points
        self.update()
        
    def pointItems(self):
        out = []
        for i in self.childItems():
            if isinstance(i,PointItem):
                out.append( i ) 
        return out
    
    def aware(self, b, scnPos):
        'return awarePoint : Scene Pos'
        if not b:
            self.prepareGeometryChange()
            self.awarePoint = None
        else:
            p = self.mapFromScene(scnPos)
            for i in self.points:
                if (p-i).manhattanLength() < 6:
                    self.prepareGeometryChange()
                    self.awarePoint = i
                    return self.mapToScene(i)
    
    def paint(self, painter, option, widget=None):
        if len(self.points )>=2:
            start = None
            for end in self.points:
                if start is not None:
                    painter.drawLine(start,end)
                start = end
        if self.isSelected():
            painter.drawRects(self._controller())
        elif self.awarePoint != None:
            rect = QRectF(self.awarePoint, self.awarePoint).adjusted(-6,-6,6,6)
            painter.drawRect(rect)
            
    def boundingRect(self):
        xs=[p.x() for p in self.points]
        ys=[p.y() for p in self.points]
        minx=min(xs)
        maxx = max(xs)
        miny = min(ys)
        maxy = max(ys)
        rect = QRectF(QPointF(minx,miny),QPointF(maxx,maxy) )
        if self.isSelected():
            rect = rect.adjusted(-self.radius,-self.radius,self.radius,self.radius)
        if self.awarePoint !=None:
            rect = rect.united(QRectF(self.awarePoint, self.awarePoint).adjusted(-6,-6,6,6))
        return rect
    
    def _controller(self):
        rects = []
        r = self.radius
        for p in self.points:
            rects.append( QRectF(p,p).adjusted(-r,-r,r,r) )
        return rects
    
    def hoverEnterEvent(self,event):
        view = event.widget()
        view.setCursor(Qt.SizeAllCursor)
        
    def hoverLeaveEvent(self,event):
        view = event.widget()
        view.setCursor(Qt.ArrowCursor)
    
    def hoverMoveEvent(self,event):
        pos = event.pos()
        view = event.widget()
        for p in self.points:
            distans = p - pos
            if distans.manhattanLength()< self.grabRadius:
                view.setCursor(Qt.PointingHandCursor)
                return 
        view.setCursor(Qt.SizeAllCursor)
            
        
    def mousePressEvent(self,event):
        self.lastpos = event.pos()
        for p in self.points:
            distans = p - event.pos()
            if distans.manhattanLength()< self.grabRadius :
                self.crt_point = p
                #self.setSelected(True)
                break  
        return s(LineStrip,event)
    
    def mouseMoveEvent(self,event):
        if self.crt_point is not None and self.lastpos is not None:
            self.prepareGeometryChange()
            dp = event.pos() - self.lastpos
            p = self.crt_point
            p.setX(p.x()+ dp.x()) 
            p.setY(p.y()+ dp.y())
            self.lastpos = event.pos()
        else:
            return s(LineStrip, event)
        
    def mouseReleaseEvent(self,event):
        if self.scene().awarePoint() != None and self.crt_point !=None:
            self.prepareGeometryChange()
            p = self.mapFromScene(self.scene().awarePoint())
            self.crt_point.setX(p.x())     
            self.crt_point.setY(p.y())  
        self.crt_point = None
        return super().mouseReleaseEvent(event)
    
    def shape(self):
        path = QPainterPath()
        
        for s,e  in self.pair(self.points):
            path.moveTo(s)
            path.lineTo(e)
        for r in self._controller():
            path.addRect(r)
        stroker = QPainterPathStroker()
        stroker.setWidth(6)
        path = stroker.createStroke(path)
        return path

    def itemChange(self,change,value):
        if change == QGraphicsItem.ItemSelectedChange:
            self.prepareGeometryChange()

        return s(LineStrip, change,value)
    
    def insertPoint(self, pos):
        'pos: self的坐标系'
        stroker = QPainterPathStroker()
        stroker.setWidth(6)
        i = 0
        for s,e in self.pair(self.points):
            i+=1
            path = QPainterPath()
            path.moveTo(s)
            path.lineTo(e)
            path = stroker.createStroke(path)
            if path.contains(pos):
                self.points.insert(i,pos)
                return
            
    def removePoint(self, pos):
        for p in self.points:
            if (p-pos).manhattanLength() <self.grabRadius:
                self.points.remove(p)
                return
            
    def pair(self, ls):
        s = None
        out = []
        for e in ls:
            if s != None:
                out.append((s,e))
            s = e
        return out
    
    def actions(self, posScen):
        if self.isSelected():
            self.msPoint = self.mapFromScene(posScen)
            return [self.act1,self.act2]
        else:
            return []
    
    def on_insert_act(self):
        if self.msPoint != None:
            self.insertPoint( self.msPoint )
            self.update()
    
    def on_rm_act(self):
        if self.msPoint != None:
            self._oldrect = self.boundingRect()
            self.removePoint(self.msPoint)
            self.update()
    
    def __reduce__(self):
        pickleDict={}
        pos = self.pos()
        points =[(i.x(),i.y()) for i in self.points]
        
        pickleDict['pos'] = (pos.x(),pos.y())
        pickleDict['points'] = points
        return self.__class__,(),pickleDict  
    
    def __setstate__(self,state):
        pos = state.pop('pos',(0,0) )
        self.setPos( *pos )
        points = state.pop('points')
        p=[]
        for x, y in points:
            p.append( QPointF(x,y))
        self.setPoints(p)
        self.__dict__.update(state)  


class LineDrawer(QObject):
    def __init__(self,scene, aware=None):
        s(LineDrawer)
        self.scene = scene
        self.aware = aware
        self.lastpoint = None
        self.lastLine = None
        self.tmplines = []
        
        self.createAct = QAction('画线',self)
        self.compAct = QAction('完成', self)
        self.createAct.triggered.connect(self.createLine)
        self.compAct.triggered.connect(self.finish)
   
    def setAware(self,aware):
        self.aware = aware
       
    def mouseMoveEvent(self, event):
        if self.lastpoint !=None and self.lastline !=None:
            point =  event.scenePos()
            self.lastline.setLine(self.lastpoint.x(),self.lastpoint.y(), point.x(),point.y() )
        return True
    
    def mouseReleaseEvent(self,  event):
        return False
    
    def createLine(self):
        self.scene.drawer = self
        
    def actions(self):
        # 有lastpoint表明是绘制状态，没有表示不是绘制状态。
        if self.lastpoint:
            return [self.compAct,]
        else:
            return [self.createAct,]

    def mousePressEvent(self, event):
        #scene = self.manager.scene
        if self.aware.awarePoint() != None:
            p = self.aware.awarePoint()
        else:
            p =  event.scenePos() 
        if self.lastpoint == None:
            self.tmppoints=[]
        else:
            if self.lastline:
                self.lastline.setLine(self.lastpoint.x(),self.lastpoint.y(), p.x(),p.y() )
                 
        self.lastline = QGraphicsLineItem(p.x(), p.y(), p.x(), p.y())
        #else:
            #view.lastline = QGraphicsLineItem(view.lastpoint.x(), view.lastpoint.y(), p.x(), p.y())
        self.tmppoints.append(p) 
        self.lastpoint = p
        self.scene.addItem(self.lastline)
        self.tmplines.append(self.lastline)
        #return func(view,event)
        return True
        
    def finish(self):
        #scene = self.manager.scene
        del self.tmppoints[-1]
        strip = LineStrip(self.tmppoints)
        self.scene.addItem(strip)
        self.tmppoints = []
        self.lastpoint = None
        #self.drawer = None
        for line in self.tmplines:
            self.scene.removeItem(line)
        self.tmplines = []
        self.scene.drawer = None
        

class Controlable:
    """能够自动添加控制杆
    子类只需要重写setSize"""
    
    def __init__(self,*args,**kw):
        s(Controlable, *args,**kw)
        self.controller = None
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
    
    def itemChange(self,change,value):
        if change == QGraphicsItem.ItemSelectedHasChanged:
            if value:
                self.controller = ControlRect(self)
            elif self.controller:
                self.scene().removeItem(self.controller)
                self.controller = None
                
        return s(Controlable, change, value)
    
    def setSize(self,qrect):
        print('需要重写AwareItem.setSize')   


class TryItem(Controlable, QGraphicsRectItem):
 
    def setSize(self,qrect):
        if qrect:
            self.setRect(qrect)

    def mouseDoubleClickEvent(self,event):
        print('双击了我')
        return s(TryItem,event)
    

class PointItem(QGraphicsItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__aware = False
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        
    def setAware(self,b):
        self.__aware =b
        self.update()
        
    def aware(self):
        return self.__aware
        
    def paint(self, painter, option, widget=None):
        if self.__aware:
            painter.drawRect(self.boundingRect())
            
    def boundingRect(self):
        return QRectF(-5,-5,10,10)
    
    def hoverEnterEvent(self,event):
        self.__aware = True
        self.update()
    
    def hoverLeaveEvent(self,event):
        if not self.parentItem().isSelected():
            self.__aware = False
            self.update()
        
    def hoverMoveEvent(self,event):
        pos = event.pos()
        view = event.widget()
        view.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self,event):
        #if self.parentItem().isSelected():
        #self.lastpos = event.pos()
        return super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        #if self.parentItem().isSelected():
        self.setPos(self.mapToParent(event.pos()) )
        self.parentItem().prepareGeometryChange()
        return super().mouseMoveEvent(event)
    
    #def mouseReleaseEvent(self, event):
        

    
    