from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from heQt.itemView import TableView
from heQt.itemModel import StdItemModel
import sys

class MyWin(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScene(QGraphicsScene())
        
         
        
        #self.setDragMode(QGraphicsView.ScrollHandDrag)
        #for i in range(10):
            #item = QGraphicsRectItem(QRectF(0,0,100,100))
            #item.setFlag(QGraphicsItem.ItemIsMovable,True )   
            #item.setPos(0,i*50)
            #self.scene().addItem(item)
        mw = MoveWin(QRectF(0,0,100,10) )
        self.scene().addItem(mw)
        
    
            
    
    def wheelEvent(self,event):
        factor = event.angleDelta().y() / 150
        if factor < 0:
            factor = 1/(-factor)
        self.scale(factor, factor)
        
class MoveWin(QGraphicsRectItem):
    def __init__(self, *args,**kw):
        super().__init__(*args,**kw)
        #item = QGraphicsRectItem(QRectF(0,0,100,10))
        #item.setParentItem(self)
        v = TableView()
        mode = StdItemModel()
        v.setModel(mode)
        for i in ['dog','pig','zip','hash']:
            mode.appendRow([QStandardItem(i),QStandardItem(i)])
        prox = QGraphicsProxyWidget()
        self.prox = prox
        
        prox.setWidget(v)
        #prox.setFlag( QGraphicsItem.ItemIsMovable,True )    
        prox.setParentItem(self)
        prox.setPos(0,12)
        self.setFlag(QGraphicsItem.ItemIsMovable,True )  
        
        self.w_height = 500
        self.w_width = 300
        self.prox.widget().resize(self.w_width,self.w_height)
        
        bot = Bottom(QRectF(0,self.w_height+20,100,10))
        self.bot = bot
        bot.setParentItem(self)
        bot.setFlag(QGraphicsItem.ItemIsMovable,True)
        bot.funcs.append(self.set_height)
        
    def set_height(self):
        print(self.bot.pos() )
        new_height = self.w_height + self.bot.pos().y() 
        self.prox.widget().resize(self.w_width,new_height)
        
    #def boundingRect(self):
        #rect = super().boundingRect()
        #print(rect)
        #rect = rect.united(self.prox.boundingRect())
        #rect.adjust(-5,-5,5,5)
        #return rect
#class innWin(QGraphicsProxyWidget):
    #def __init__(self,*args,**kw):
        #super().__init__(*args,**kw)
    
    #def boundingRect(self):
        #rect = super().boundingRect()
        #rect.adjust(-5,-5,5,5)
        #return rect
class Bottom(QGraphicsRectItem):
    funcs = []
    def mouseMoveEvent(self,event):
        super().mouseMoveEvent(event)
        for i in self.funcs:
            i()
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyWin()
    win.show()
    sys.exit(app.exec_())