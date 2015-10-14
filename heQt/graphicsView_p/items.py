from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from functools import partial
    

class ControlRect(QGraphicsItem):
    """
    控制方框。
    """
    def __init__(self, item, qrect = None ,parentItem=None):
        super().__init__(parentItem)
        self.controllerRadius = 6
        self.margin = self.controllerRadius
        self.item = item
        self.lastPos = None
        self.msState = -1
        self._oldrect = None
        
        self.setParentItem(item)
        #item.scene().addItem(self)
        #item.moveObserver.append(self.setPos)
        #pitem = item.parentItem()
        #if pitem:
            #self.setPos(pitem.mapToScene(item.pos()))
        #else:
            #self.setPos(item.pos())
        self.rect = qrect if qrect else item.boundingRect()
        
        # 本来不需要 movable的，但是为了和下面的item抢事件，所以设置了个Movable
        self.setFlag(QGraphicsItem.ItemIsMovable)

    def resize(self,qrect):
        if not self._oldrect:
            self._oldrect = self.rect.adjusted(-self.margin,-self.margin,self.margin,self.margin)
        else:
            self._oldrect = self._oldrect.united(self.rect)
            
        self.rect = qrect
        self.update()
        self.setSize(qrect)

    def setSize(self, qrect = None):
        if hasattr(self.item,'setSize'):
            self.item.setSize(qrect)
                
    def boundingRect(self):
        if self._oldrect:
            return self._oldrect
        else:
            
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
        elif self.lastPos:
            rect = self.rect
            dx ,dy =event.pos().x()-self.lastPos.x() , event.pos().y()-self.lastPos.y() 
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
            
            self.lastPos+= QPointF(dx,dy) 
            self.resize(rect)
            
    def mousePressEvent(self,event):
        self.lastPos = event.pos()
        return super().mousePressEvent(event)
    
    def mouseReleaseEvent(self,event):
        self.lastPos = ''
        return super().mouseReleaseEvent(event)
    
    def paint(self, painter, option, widget=None):
        if self._oldrect:
            self.scene().update(self.mapToScene( self._oldrect).boundingRect() )
            self._oldrect = None
        painter.drawRect(self.rect)
        for i in self._controller():
            painter.fillRect(i,QColor('black') ) 
    
    def MSFreeMove(self,pos,view):
        pos = self.mapFromScene(pos)
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

#class Line(QGraphicsItem):
    
    #def __init__(self, p1, p2, parent=None):
        #super().__init__(parent)
        #self.p1 = p1
        #self.p2 = p2
        
    #def boundingRect(self):
        #x = [self.p1.x(), self.p2.x()]
        #y = [self.p1.y(), self.p2.y()]
        #minx=min(x)
        #maxx = max(x)
        #miny = min(y)
        #maxy = max(y)
        #rect = QRectF(QPointF(minx,miny),QPointF(maxx,maxy) )
        ##if self.isSelected():
            ##rect = rect.adjusted(-self.radius,-self.radius,self.radius,self.radius)
        ##if self._oldrect:
            ##rect = self._oldrect.united(rect) 
        #return rect        
    
    #def paint(self, painter, option, widget=None):
        #painter.drawLine(self.p1,self.p2)
    
    #def MSFreeMove(self, pos, view):
        #self.parentItem().MSFreeMove(pos,view)
    
    #def shape(self):
        #path = QPainterPath()
        #path.moveTo(self.p1)
        #path.lineTo(self.p2)
        #stroker = QPainterPathStroker()
        #stroker.setWidth(5)
        #path = stroker.createStroke(path)
        #return path

class LineStrip(QGraphicsItem):
    def __init__(self, points, parent=None):
        super().__init__(parent)
        self.crt_point = None
        self.radius = 6
        self.grabRadius = 10
        self.points = points
        self.msPoint = None
        self._oldrect = None
        #self.cst_lines(points)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        
        self.act1 = QAction('插入点', None)
        self.act2 = QAction('删除当前点', None)
        self.act1.triggered.connect(self.on_insert_act)
        self.act2.triggered.connect(self.on_rm_act)
    
    @staticmethod
    def rigisterView(view):
        view.mapfunc['createLine'] ={
            'mouseMoveEvent':LineStrip.viewMsMove,
            'mousePressEvent':LineStrip.viewMsPress,
            'mouseReleaseEvent':LineStrip.viewMsRelease,
            'proxyplug1':LineStrip._completLine,
            'actions':LineStrip.viewActions
        }     
        
        view.lastpoint = None
        view.tmppoints = []
        view.tmplines = []
        view.registFreeMSmoveAware(LineStrip)
        
    @staticmethod
    def viewMsPress(func, view, event):
        p = view.mapToScene( event.pos() )
        if not view.lastpoint:
            view.tmppoints=[]
        view.tmppoints.append(p)
        if view.lastpoint:
            view.lastline = QGraphicsLineItem(view.lastpoint.x(), view.lastpoint.y(), p.x(), p.y())
        else:
            view.lastline = QGraphicsLineItem(p.x(), p.y(), p.x(), p.y())
        view.lastpoint = p
        view.scene().addItem(view.lastline)
        view.tmplines.append(view.lastline)
        
    @staticmethod
    def viewMsMove( func, view, event):
        point = view.mapToScene( event.pos() )
        if view.lastpoint and view.lastline:
            view.lastline.setLine(view.lastpoint.x(),view.lastpoint.y(), point.x(),point.y() )
    
    @staticmethod
    def viewMsRelease(func, view,  event):
        return func(view,event)
        #if view.lastline:
            #view.scene().removeItem(view.lastline)
        
           #view.lastline = None
    @staticmethod
    def viewActions(func, view):
        ls = []
        if not hasattr(view,'_completline'):
            view._completline = QAction('完成',view)
            view._completline.triggered.connect(view.proxyplug1)
        ls.append(view._completline)
        ls.extend( func(view) )
        return ls
        
    @staticmethod
    def _completLine(func, view,trig):
        strip = LineStrip(view.tmppoints)
        view.scene().addItem(strip)
        view.tmppoints = []
        view.lastpoint = None
        view.dynstate = None
        for line in view.tmplines:
            view.scene().removeItem(line)
        view.tmplines = []
             
    def paint(self, painter, option, widget=None):
        if self._oldrect:
            self.scene().update(self.mapToScene( self._oldrect).boundingRect() )
            self._oldrect = None
        if len(self.points)>=2:
            start = None
            for end in self.points:
                if start is not None:
                    painter.drawLine(start,end)
                start = end
        if self.isSelected():
            painter.drawRects(self._controller())
        #painter.drawPath(self.shape())
    
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
        if self._oldrect:
            rect = self._oldrect.united(rect) 
        return rect
    
    def _controller(self):
        rects = []
        for p in self.points:
            rects.append( QRectF(p,p).adjusted(-self.radius,-self.radius,self.radius,self.radius) )
        return rects
    
    def MSFreeMove(self,pos,view):
        pos = self.mapFromScene(pos)
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
                self.setSelected(True)
                break  
        return super().mousePressEvent(event)
    
    def mouseMoveEvent(self,event):
        if self.crt_point is not None and self.lastpos is not None:
            self._oldrect = self._oldrect.united(self.boundingRect()) if self._oldrect else self.boundingRect()
            dp = event.pos() - self.lastpos
            p = self.crt_point
            p.setX(p.x()+ dp.x()) 
            p.setY(p.y()+ dp.y())
            self.lastpos = event.pos()
            self.update()
        else:
            return super().mouseMoveEvent(event)
        
    def mouseReleaseEvent(self,event):
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
            if not value:
                self.scene().update(self.mapToScene(self.boundingRect()).boundingRect() )
                
        return super().itemChange(change,value)
    
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
        
class AwareItem(QGraphicsItem):
    """能够自动添加控制杆
    子类只需要重写setSize"""
    
    @staticmethod
    def rigisterView(view):   
        view.registFreeMSmoveAware(ControlRect)    
        
    def __init__(self,*args,**kw):
        super().__init__(*args,**kw)
        self.controller = None

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
    
    def itemChange(self,change,value):
        if change == QGraphicsItem.ItemSelectedHasChanged:
            if value:
                self.controller = ControlRect(self)
            else:
                if self.controller:
                    self.scene().removeItem(self.controller)
                    self.controller = None
                
        return super().itemChange(change,value)
    
    def setSize(self,qrect):
        print('需要重写AwareItem.setSize')   

class TryItem(QGraphicsRectItem,AwareItem):
    def __init__(self, parent=None):
        super().__init__(parent)
  
    def setSize(self,qrect):
        if qrect:
            self.setRect(qrect)

    def mouseDoubleClickEvent(self,event):
        print('双击了我')
        return super().mouseDoubleClickEvent(event)
    

    
        