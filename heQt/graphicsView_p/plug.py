from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

 

class ControlRect(QGraphicsItem):
    """
    控制方框。
    """
    def __init__(self, parentItem=None):
        super().__init__(parentItem)
        self.controllerRadius = 6
        self.margin = self.controllerRadius*2
        self.lastPos = ''
        self.msState = -1
        self.oldrect = ''
        
        #self.rect = qrect if qrect else item.boundingRect()
        self.innRect = self.boundingRect()
        self.setFlag(QGraphicsItem.ItemIsMovable)
        
    def resize(self,qrect):
        if not self.oldrect:
            self.oldrect = self.innRect.adjusted(-self.margin,-self.margin,self.margin,self.margin)
        else:
            self.oldrect = self.oldrect.united(self.innRect)
            
        self.innRect = qrect
        self.update()
        self.setSizePos(qrect=qrect)

    def setSizePos(self,qrect = None,pos =None):
        if hasattr(self.item,'setSizePos'):
            self.item.setSizePos(qrect=qrect,pos=pos)  
                

    def modifyBDRect(self,rect):
        if self.isSelected():
            self.innRect = rect
            if self.oldrect:
                return self.oldrect
            else:
                rect = rect.adjusted(-self.margin,-self.margin,self.margin,self.margin)
                return rect
        else:
            return rect
        
    def _controller(self):
        tl,tr,bl,br = self.innRect.topLeft(),self.innRect.topRight(),self.innRect.bottomLeft(),self.innRect.bottomRight()
        tm = QPointF(tl.x()+(tr.x()-tl.x())/2,tl.y())
        ml, mr = QPointF(bl.x(),tl.y()+(bl.y()-tl.y())/2), QPointF(br.x(),tr.y()+(br.y()-tr.y())/2)
        bm = QPointF(bl.x()+(br.x()-bl.x())/2, bl.y())
        ls = [tl,tm,tr,ml,mr,bl,bm,br]
        out = []
        for i in ls:
            out.append( QRectF(i.x()-self.controllerRadius,i.y()-self.controllerRadius,self.controllerRadius*2,self.controllerRadius*2) )
        return out
    
    def mouseMoveEvent(self,event):
        if self.msState ==-1:
            self.setSizePos(pos=self.pos())
            return super().mouseMoveEvent(event)
        elif self.lastPos:
            rect = self.innRect
            dx ,dy =event.pos().x()-self.lastPos.x() , event.pos().y()-self.lastPos.y() 
            if self.msState == 0:
                if dy > 0 and self.innRect.height() < 10:
                    dy = 0
                if dx > 0 and self.innRect.width() < 10:
                    dx = 0
                rect = self.innRect.adjusted(dx,dy,0,0)
            elif self.msState == 1:
                if dy > 0 and self.innRect.height()<10:
                    dy =0
                rect = self.innRect.adjusted(0,dy,0,0)
            elif self.msState == 2:
                if dx < 0 and self.innRect.width() < 10:
                    dx = 0
                if dy > 0 and self.innRect.height()<10:
                    dy = 0 
                rect = self.innRect.adjusted(0,dy,dx,0)
            elif self.msState == 3:
                if dx >0 and self.innRect.width() <10:
                    dx = 0
                rect = self.innRect.adjusted(dx,0,0,0)
            elif self.msState == 4:
                if dx <0 and self.innRect.width() <10:
                    dx = 0
                rect = self.innRect.adjusted(0,0,dx,0)
            elif self.msState ==5:
                if dx>0 and self.innRect.width()<10:
                    dx =0
                if dy <0 and self.innRect.height()<10:
                    dy = 0
                rect = self.innRect.adjusted(dx,0,0,dy)
            elif self.msState ==6:
                if dy <0 and self.innRect.height()<10:
                    dy =0
                rect =self.innRect.adjusted(0,0,0,dy)
            elif self.msState == 7:
                if dx <0 and self.innRect.width()<10:
                    dx =0
                if dy <0 and self.innRect.height() <10:
                    dy =0
                rect =self.innRect.adjusted(0,0,dx,dy)
            

            self.lastPos+= QPointF(dx,dy) 
            #self.resize(rect)
            
            #if self.msState == -1:
                #self.setSizePos(pos=self.pos())
                #pos = self.pos()+ QPointF(dx,dy)
                #print(dx,dy)
                #print(pos)
                #self.setPos(pos)
            

    
    def mousePressEvent(self,event):
        self.lastPos = event.pos()
        return super().mousePressEvent(event)
    
    def mouseReleaseEvent(self,event):
        self.lastPos = ''
        return super().mouseReleaseEvent(event)
    
    def paint(self, painter, option, widget=None):
        if self.isSelected():
            if self.oldrect:
                painter.eraseRect(self.oldrect)
                self.oldrect = None
            painter.drawRect(self.innRect)
            for i in self._controller():
                painter.fillRect(i,QColor('black') )
        #return super().paint(painter, option, widget)
    
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

#class AwareItem:
    #def __init__(self,*args,**kw):
        #super().__init__(*args,**kw)
        #self.controller = ''
        #self.selectObserver=[]
        
        #self.setFlag(QGraphicsItem.ItemIsSelectable)
        #self.selectObserver.append(self.on_selected)   
        
    #def selectChangNotify(self,is_selected):
        #for i in self.selectObserver:
            #i(is_selected)

    #def on_selected(self,is_selected):
        #if is_selected:
            #self.controller = ControlRect(self)
        #elif not is_selected:
            #if self.controller:
                #self.scene().removeItem(self.controller)

#class TryItem(QGraphicsRectItem,AwareItem):
    #def __init__(self, parent=None):
        #super().__init__(parent)
  
    #def setSizePos(self,qrect,pos):
        #if qrect:
            #self.setRect(qrect)
        #elif pos:
            #pos =self.mapFromScene(pos)
            #ppos= self.mapToParent(pos)
            #self.setPos(ppos)

class TryItem(QGraphicsRectItem):

    
    def boundingRect(self):
        print('kkk')
        return self.modifyBDRect(super().boundingRect())
        