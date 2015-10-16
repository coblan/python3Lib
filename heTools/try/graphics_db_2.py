from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from dg import Ui_Dialog
from heQt.graphicsView import GraphicsView
from heOs.pickle_ import IPickle
import pickle,os
import sys
from syntext import SynModel
from saveToApp import reguler_code
from parse_model import parse,App,model
from heStruct.cls import dynplug
from heQt.graphicsView_p.items import LineStrip

class MyWin(GraphicsView):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pickleable = (ModelGram,QGraphicsLineItem,AppGram,Text,Rect,LineStrip)
        gob .win= self
        self.state = ''
        self.tmp_line = ''
        self.tmp_rect = ''
        self.pars_fname = ''
        self.start_pos = ''
        self.setScene(QGraphicsScene())
        
        #self.scene().installEventFilter(self)
        
        #self.setDragMode(QGraphicsView.RubberBandDrag)
        self.set_band()
        
        #self.setContextMenuPolicy(Qt.ActionsContextMenu)
        acts =[('删除当前item',self.rm_under_ms_itm),
               ('添加model',self.add_model),
               ('添加app',self.add_app),
               ('',''),
               ('框选',self.set_band),
               ('手抓',self.set_hand),
               ('',''),
               ('copy',self.copy_selected),
               ('paest',self.paest),
               ('',''),
               ('切换选中项状态',self.toggle_state),
               ('导出选中项',self.extract_from_sel)]
        
        
        for n,f in acts:
            act = QAction(n,self)
            if not n:
                act.setSeparator(True)
            else:
                act.triggered.connect(f)
            self.addAction(act)
            
    def toggle_state(self):
        sels = self.scene().selectedItems()
        for i in sels:
            if isinstance(i,Gram):
                i.active = not i.active
                i.update()
                   
    def copy_selected(self):
        sels = self.scene().selectedItems()
        sels = [i for i in sels if isinstance(i,self.pickleable)]
        mime = QMimeData()
        mime.setData('byte/Gram',QByteArray(pickle.dumps(sels)) )
        QApplication.clipboard().setMimeData(mime)
        
    def paest(self):
        qbyt = QApplication.clipboard().mimeData().data('byte/Gram')
        byt = qbyt.data()
        if byt:
            sels = pickle.loads(byt)
            for i in sels:
                self.scene().addItem(i)
    
    def set_band(self):
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setInteractive(True)
        
    def set_hand(self):
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setInteractive(False)
        
    def rm_under_ms_itm(self):
        sels = self.scene().selectedItems()
        if sels:
            for i in sels:
                self.scene().removeItem(i)
        elif self.under_ms_item:
            self.scene().removeItem(self.under_ms_item)
            
    def contextMenuEvent(self,event):
        self.show_ctx(event.pos())
  
        
    def show_ctx(self,pos):
        self.under_ms_item = self.itemAt(pos)
        self.menu = QMenu()
        if hasattr(self.under_ms_item,'actions') :
            self.menu.addActions(self.under_ms_item.actions(posScen = self.mapToScene(pos)))
        self.menu.addActions(self.actions())
        self.menu.exec_(self.viewport().mapToGlobal(pos)) 
        
    def set_line(self):
        self.dynstate = 'create_linestrip'
        #if self.sender().isChecked():
            #self.state = 'draw_line'
        #else:
            #self.state = ''
    def set_rect(self):
        if self.sender().isChecked():
            self.state = 'draw_rect'
        else:
            self.state = ''
    
    @dynplug
    def mousePressEvent(self,event):
        if self.state == 'draw_line':
            self.start_pos = self.mapToScene( event.pos() )
        elif self.state == 'draw_rect':
            self.start_pos = self.mapToScene( event.pos() )
            
        return super().mousePressEvent(event)
    
    @dynplug
    def mouseMoveEvent(self,event):
        if self.state == 'draw_line' and self.start_pos:
            if self.tmp_line:
                self.scene().removeItem(self.tmp_line)
            pos = self.mapToScene( event.pos() )
            self.tmp_line = QGraphicsLineItem(self.start_pos.x(),self.start_pos.y(),pos.x(),pos.y())
            self.scene().addItem(self.tmp_line)
        elif self.state == 'draw_rect' and self.start_pos:
            if self.tmp_rect:
                self.scene().removeItem(self.tmp_rect)
            pos = self.mapToScene( event.pos() )
            rectf = self.ponit2rectf(self.start_pos , pos)
            self.tmp_rect = QGraphicsRectItem(rectf)
            self.scene().addItem(self.tmp_rect)
            
        else:
            return super().mouseMoveEvent(event)
    def ponit2rectf(self,p1,p2):
        x1 ,y1 = min( p1.x(),p2.x()) ,min(p1.y(),p2.y())
        x2,y2 =  max( p1.x(),p2.x()) ,max(p1.y(),p2.y())
        return QRectF( QPointF(x1,y1),QPointF(x2,y2))
        
    @dynplug
    def mouseReleaseEvent(self,event):
        if self.state == 'draw_line' and self.start_pos:
            if self.tmp_line:
                self.scene().removeItem(self.tmp_line) 
                self.tmp_line = ''
            pos = self.mapToScene( event.pos() )
            line =Line(self.start_pos.x(),self.start_pos.y(),pos.x(),pos.y())
            self.scene().addItem(line)
            self.start_pos = ''
        elif self.state == 'draw_rect' and self.start_pos:
            if self.tmp_rect:
                self.scene().removeItem(self.tmp_rect)
                self.tmp_rect = ''
            pos = self.mapToScene( event.pos() )
            rectf = self.ponit2rectf(self.start_pos , pos)
            rect = Rect(rectf)    
            self.scene().addItem(rect)
            self.start_pos = ''
        return super().mouseReleaseEvent(event)
    
    def save(self):

        if not self.pars_fname:
            return self.save_as()

        out = []
        for i in  self.scene().items():
            if isinstance(i,self.pickleable):
                out.append(i)
        with open(self.pars_fname,'wb') as f:
            pickle.dump(out,f)
            
    def save_as(self):
        name,ok = QFileDialog.getSaveFileName(None,'保存解析文件为')
        if name:
            self.pars_fname = name
            self.save()
    
    def load(self):
        name ,ok = QFileDialog.getOpenFileName(None,'打开解析文件')
        if os.path.exists(name):
            self.scene().clear()
            self.pars_fname = name
            with open(name,'rb') as f:
                items = pickle.load(f)
                for i in items:
                    self.scene().addItem(i)
                    
    #def add(self):
        #mw = ModelGram('new title','new item','')
        #self.scene().addItem(mw)   
        
        #title = QGraphicsTextItem()
        #title.setPlainText('dpog')
        #title.setTextInteractionFlags(Qt.TextEditorInteraction)  
        #self.scene().addItem(title)
    def add_model(self):
        mw = ModelGram('new title','new item','')
        self.scene().addItem(mw)  
    def add_app(self):
        m_app = AppGram('new app', 'code')
        self.scene().addItem(m_app)
        
    #def from_dict(self,dc):
        #for k ,v in dc.items():
            #item = ModelGram(k)
            #item.code = v
            #self.scene().addItem(item)

    def parser(self):
        name = QFileDialog.getExistingDirectory(None,'选择文件夹')
        if os.path.exists(name):
            self.pars_fname = ''
            ls = parse(name)
            self.scene().clear()
            #self.from_dict(dc)
            for i in ls:
                if isinstance(i,model):
                    self.scene().addItem( ModelGram(i.app, i.name,i.code) )
                elif isinstance(i,App):
                    self.scene().addItem(AppGram(i.name,i.code))
    def update_cst(self):
        name = QFileDialog.getExistingDirectory(None,'选择文件夹')
        if os.path.exists(name):
            self.pars_fname = ''
            ls = parse(name)
            for i in ls:
                gram = self.find_gram(i)
                if gram:
                    gram.code = i.code
                else:
                    if isinstance(i,model):
                        self.scene().addItem( ModelGram(i.app, i.name,i.code) )
                    elif isinstance(i,App):
                        self.scene().addItem(AppGram(i.name,i.code))   
    def add_cst(self):
        name = QFileDialog.getExistingDirectory(None,'选择文件夹')
        if os.path.exists(name):
            self.pars_fname = ''
            ls = parse(name)
            for i in ls:
                gram = self.find_gram(i)
                if gram:
                    continue
                else:
                    if isinstance(i,model):
                        self.scene().addItem( ModelGram(i.app, i.name,i.code) )
                    elif isinstance(i,App):
                        self.scene().addItem(AppGram(i.name,i.code))        
                    
    def find_gram(self,obj):
        if isinstance(obj,model):
            for i in self.walk_type(ModelGram):
                if i.app()== obj.app and i.name()== obj.name:
                    return i
        elif isinstance(obj,App):
            for i in self.walk_type(AppGram):
                if i.name()==obj.name:
                    return i
        
    def walk_type(self,tp):
        for i in self.scene().items():
            if isinstance(i,tp):
                yield i
                
    def to_app(self):
        dir_name = QFileDialog.getExistingDirectory(None,'app文件夹')
        if not dir_name:
            return
        apps,models =[],[]
        for i in self.scene().items():
            if isinstance(i,ModelGram):
                models.append(i)
            elif isinstance(i,AppGram):
                apps.append(i)
        for app_ in apps:
            if not app_.active:
                continue
            dir_app = os.path.join(dir_name,app_.name() )
            modelpy = os.path.join(dir_app,'models.py')
            try:
                os.mkdir(dir_app)
            except OSError:
                pass
            with open(modelpy ,'w',encoding='utf8') as f:
                f.write(app_.code )
        
        for model in models:
            if not model.active:
                continue
            dir_app = os.path.join(dir_name,model.app() )
            modelpy = os.path.join(dir_app,'models.py')
            reg_code = reguler_code(model.code)+ '\n'
            with open(modelpy,'a',encoding= 'utf8') as f:
                f.write(reg_code)
                
    def extract_from_sel(self):
        dir_name = QFileDialog.getExistingDirectory(None,'app文件夹')
        if not dir_name:
            return
        apps,models =[],[]
        for i in self.scene().items():
            if isinstance(i,ModelGram):
                models.append(i)
            elif isinstance(i,AppGram):
                apps.append(i)
        for app_ in apps:
            if not app_.isSelected():
                continue
            dir_app = os.path.join(dir_name,app_.name() )
            modelpy = os.path.join(dir_app,'models.py')
            try:
                os.mkdir(dir_app)
            except OSError:
                pass
            with open(modelpy ,'w',encoding='utf8') as f:
                f.write(app_.code )
        
        for model in models:
            if not model.isSelected():
                continue            
            dir_app = os.path.join(dir_name,model.app() )
            modelpy = os.path.join(dir_app,'models.py')
            reg_code = reguler_code(model.code)+ '\n'
            with open(modelpy,'a+',encoding= 'utf8') as f:
                f.write(reg_code)
                
                
    def insert_text(self):
        t = Text('新的说明')
        self.scene().addItem(t)

        

class gob(object):
    win = ''

class Line(QGraphicsLineItem,IPickle):
    def __init__(self, x1,y1,x2,y2):
        super().__init__(x1,y1,x2,y2)
        self.constructArgs =(x1,y1,x2,y2)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)        
    def __reduce__(self):
        self.pickleDict['pos'] = self.pos()
        return self.__class__,self.constructArgs,self.pickleDict  
    def __setstate__(self,state):
        self.setPos(state.pop('pos',QPoint(0,0)) )
        self.__dict__.update(state)    

from heQt.graphicsView_p.items import AwareItem,ControlRect
class Gram(AwareItem,IPickle):
    
    def __init__(self,*args,**kw):
        super().__init__(*args,**kw)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)  
        
        self.dialog = mydg(gob.win)
        self.active = True
        
        self.dialog.resize(700,700)
        #self.dialog.setWindowFlags(self.dialog.windowFlags()|Qt.Tool)
        self.dialog.accepted.connect(self.on_dialog_accepted)
    
      
    def on_dialog_accepted(self):
        self.code = self.dialog.plainTextEdit.toPlainText()
        
    def open_code(self):
        #dd=mydg()
        self.dialog.setWindowTitle(self.get_title())
        self.dialog.plainTextEdit.setPlainText(self.code)
        self.dialog.show()
        #if dd.show() == QDialog.Accepted:
            #self.code = dd.plainTextEdit.toPlainText()    
            
    def boundingRect(self):
        rect = QRectF()
        for i in self.childItems():
            if isinstance(i,ControlRect):
                continue
            rect_tmp = i.mapRectToParent(i.boundingRect())
            rect = rect.united(rect_tmp)
        return rect 
    
    #def actions(self):
        #return self.actls   
    def mouseDoubleClickEvent(self,event):
        self.open_code()
        #for i in [self.title,self.name]:
            #if i.mapToParent(i.boundingRect()).containsPoint( event.pos(),0):
                #i.start_edit()
        #return super().mouseDoubleClickEvent(event)   
    def get_title(self):
        return ''
    
    def paint(self,painter, option, widget=None):
        if not self.active:
            painter.setBrush(QColor('red'))
        else:
            painter.setBrush(QColor('green'))
        painter.drawEllipse(QRectF(0,0,10,10))
        
        #return super().paint(painter, option, widget)
        
class ModelGram(Gram):
    def __init__(self,title,name,code,*args,**kw):
        super().__init__(*args,**kw)
        self.code = code
        
        self.title_label = textlable()
        self.title_label.setPlainText(title)
        font1,font2 = QFont(),QFont()
        font1.setPixelSize(12)
        font2.setPixelSize(15)
        font2.setBold(True)
        self.title_label.setFont(font1)
        self.name_label = textlable()
        self.name_label.setPlainText(name)
        #self.name.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.name_label.setPos(0,30)
        self.name_label.setFont(font2)
        self.title_label.setParentItem(self)
        self.name_label.setParentItem(self)
        #self.addToGroup(self.title)
        #self.addToGroup(self.name)
 
        self.title_label.edited.connect(self.update)
        self.name_label.edited.connect(self.update)
    #def actions(self):
        #return self.lable.actions()

            
    def __reduce__(self):
        #self.pickleDict['code'] = self.code
        self.pickleDict['pos'] = self.pos()
        self.pickleDict['active'] = self.active
        return self.__class__,(self.title_label.toPlainText(),self.name_label.toPlainText(),self.code,),self.pickleDict    
    def __setstate__(self,state):
        self.setPos(state.pop('pos',QPoint(0,0)) )
        self.active = state.pop('active',True)
        self.__dict__.update(state)

    def paint(self,painter, option, widget = None):
        rect = self.boundingRect()
        painter.drawRect(rect)
        
        painter.drawLine(rect.x(),rect.y()+20,rect.width(),rect.y()+20)
        super().paint(painter, option, widget)
         
    def get_title(self):
        return self.title_label.toPlainText()+ '__' + self.name_label.toPlainText()
   
    def name(self):
        return self.name_label.toPlainText()
    def app(self):
        return self.title_label.toPlainText()
    
    #def sceneEvent(self,event):
        
        #if self.title.hasFocus():
            #if event.type() == QEvent.GraphicsSceneMouseMove:
                #self.scene().sendEvent(self.title,event)
                #return
        #return super().sceneEvent(event)
    #def mouseDoubleClickEvent(self,event):
        #for i in [self.title,self.name]:
            #if i.mapToParent(i.boundingRect()).containsPoint( event.pos(),0):
                #i.start_edit()
        #return super().mouseDoubleClickEvent(event)
    
class textlable(QGraphicsTextItem):
    edited = pyqtSignal()
    def __init__(self, *args,**kw):
        super().__init__(*args,**kw)
        #self.setTextInteractionFlags(Qt.TextEditorInteraction)
        #self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.edit = QLineEdit(gob.win)
        self.edit.editingFinished.connect(self.hideEdit)
        
        self.act1 = QAction('编辑',gob.win)
        self.act1.triggered.connect(self.start_edit)
        
        
    def start_edit(self):
        #self.edit.setParent()
        rect = self.mapRectToScene(self.boundingRect())
        rect = gob.win.mapFromScene(rect).boundingRect()
        self.edit.setGeometry(rect)
        self.edit.setText(self.toPlainText())
        self.edit.show()
        self.edit.setFocus(True)
        
    def hideEdit(self):
        self.edit.hide()
        self.setPlainText(self.edit.text())
        self.edited.emit()

    def actions(self):
        self.act1.setText('编辑_%s'%self.toPlainText())
        return [self.act1,]
        #p = self.parentItem()
        #if hasattr(p,'actions'):
            #return p.actions()
class Text(textlable):
    def __init__(self,*args):
        super().__init__(*args)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable) 

    def __reduce__(self):
        pk = {}
        pk['text'] = self.toPlainText()
        pk['pos'] =self.pos()
        return self.__class__ , tuple() ,pk
    
    def __setstate__(self,state):
        self.setPlainText(state.pop('text'))
        self.setPos(state.pop('pos'))
        
    def mouseDoubleClickEvent(self,event):
        self.start_edit()

class ProxySignal(QObject):
    def __init__(self,func):
        super().__init__()
        self.func = func
    def bridge(self):
        self.func( self.sender().text() )
        
class Rect(QGraphicsRectItem):
    def __init__(self,*args):
        super().__init__(*args)
        self.bg_color = '#F8F8FF'
        self.setZValue(-100)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable) 
        
        self.signal_color = ProxySignal(self.set_bg_color)
        acts_color=['#F8F8FF','#FFE1FF','#E0FFFF',]
        self.acts = []
        for i in acts_color:
            act= QAction(i,gob.win)
            pix = QPixmap(30,30)
            pix.fill(QColor(i))      
            act.setIcon(QIcon(pix))
            act.triggered.connect(self.signal_color.bridge)
            self.acts.append(act)
        
        act2 = QAction('放到底层',gob.win)
        act2.triggered.connect(self.add_z)
        self.acts.append(act2)
        act3 = QAction('',gob.win)
        act3.setSeparator(True)
        self.acts.append(act3)
    
    def add_z(self):
        self.setZValue(self.zValue()-1)
        
    def __reduce__(self):
        pk = {}
        pk['rect'] = self.rect()
        pk['pos'] =self.pos()
        pk['bg_color'] = self.bg_color
        pk['z'] =self.zValue()
        return self.__class__ , tuple() ,pk
    
    def __setstate__(self,state):
        self.setRect(state.pop('rect'))
        self.setPos(state.pop('pos'))
        self.set_bg_color(state.pop('bg_color','#F8F8FF'))
        self.setZValue(state.pop('z',-100))
    def paint(self,Painter, Option, widget=None):
        Painter.fillRect(self.boundingRect(),QColor(self.bg_color))
        Painter.setPen(QColor('#E8E8E8'))
        Painter.drawRect(self.boundingRect())
        return super().paint(Painter, Option, widget)
    
    def actions(self):
        return self.acts
    def set_bg_color(self,color):
        self.bg_color = color
        self.update()
        
class AppGram(Gram):
    def __init__(self,name,code,*args,**kw):
        super().__init__(*args)
        self.label = textlable()
        self.label.setPlainText(name)
        self.label.setParentItem(self)
        self.label.edited.connect(self.update)
        
        self.code = code
        
    def __reduce__(self):
        #self.pickleDict['code'] = self.code
        self.pickleDict['pos'] = self.pos()
        self.pickleDict['active'] = self.active
        return self.__class__,(self.label.toPlainText(),self.code,),self.pickleDict    
    def __setstate__(self,state):
        self.setPos(state.pop('pos',QPoint(0,0)) )
        self.active = state.pop('active',True)
        self.__dict__.update(state)
    def name(self):
        return self.label.toPlainText()
    #def mouseDoubleClickEvent(self,event):
        #for i in [self.name,]:
            #if i.mapToParent(i.boundingRect()).containsPoint( event.pos(),0):
                #i.start_edit()
        #return super().mouseDoubleClickEvent(event)
    
    def paint(self,painter, option, widget = None):
        rect = self.boundingRect()
        painter.setPen(QColor('blue'))
        painter.drawRect(rect)
        #painter.drawLine(rect.x(),rect.y()+20,rect.width(),rect.y()+20)  
        return super().paint(painter, option, widget)
    
    def get_title(self):
        return self.label.toPlainText()
        
class mydg(QDialog,Ui_Dialog):
    def __init__(self,*args, **kw):
        super().__init__(*args,**kw)
        self.setupUi(self)
        self.syn = SynModel( self.plainTextEdit.document() )
    
    #def mouseDoubleClickEvent(self,event):
        #rt = super().mouseDoubleClickEvent(event)
        #print( self.plainTextEdit.textCursor().selectedText() )
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwin =QMainWindow()
    win = MyWin()
    #win.add_pickle()
    
    mainwin.setCentralWidget(win)
    mainwin.show()

    
    act1 = QAction('line',mainwin)
    act_txt = QAction('说明文字',mainwin)
    act_rect = QAction('框',mainwin)
    #act1.setCheckable(True)
    act_rect.setCheckable(True)
    act_save = QAction('save',mainwin)
    act_save_as = QAction('save as',mainwin)

    act_parser = QAction('parser',mainwin)
    act_update_cst = QAction('更新结构',mainwin)
    act_add_cst = QAction('添加结构',mainwin)
    act_load = QAction('load',mainwin)
    act_to_app = QAction('to_app',mainwin)
    
    act1.triggered.connect(win.set_line)
    act_txt.triggered.connect(win.insert_text)
    act_rect.triggered.connect(win.set_rect)
    act_save.triggered.connect(win.save)
    act_save_as.triggered.connect(win.save_as)
    act_parser.triggered.connect(win.parser)
    act_update_cst.triggered.connect(win.update_cst)
    act_add_cst.triggered.connect(win.add_cst)
    act_load.triggered.connect(win.load)
    act_to_app.triggered.connect(win.to_app)
    
    tb=QToolBar()
    tb.addAction(act1)
    tb.addAction(act_txt)
    tb.addAction(act_rect)
    tb.addAction(act_save)
    tb.addAction(act_save_as)
    #tb.addAction(act_add)
    tb.addAction(act_parser)
    tb.addAction(act_update_cst)
    tb.addAction(act_add_cst)
    tb.addAction(act_load)
    tb.addAction(act_to_app)
    
    mainwin.addToolBar(tb)
    
    
    #from parse_model import get_dict
    
    #win.from_dict(get_dict())
    
    
    sys.exit(app.exec_())    