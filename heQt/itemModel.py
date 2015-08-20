# -*- coding: utf-8 -*-
#
# 主要添加功能包括：
# 1. 直接保存到文件，从文件读取恢复。注意item必须使用item.py中的stdItem

from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from heOs.pickle_ import IPickle
from heQt.item import stdItem
import itertools

##def adapt(mode):
##    '''适配器，用于调整save和open函数的参数，
##    使得其可以接受string和datastream类型'''
##    def _realFun(fun):
##        def realFun(self,data):
##            if isinstance(data, str):
##                f=QFile(data)
##                f.open(mode)
##                stream=QDataStream(f)
##                fun(self,stream)
##            elif isinstance(data, QDataStream):
##                fun(self,data)
##            else:
##                raise TypeError("arg need a string or qdatastream")
##        return realFun
##    return _realFun

##def recurSave(item,cout):
##    row,col=item.rowCount(),item.columnCount()
##    cout.writeQVariant([row,col])
##    for ri in range(row):
##        for ci in range(col):
##            if item.child(ri,ci):
##                cout.writeBool(True)
##                cout.writeInt32(ri)
##                cout.writeInt32(ci)
##                cout<<item.child(ri,ci)
##                recurSave(item.child(ri,ci),cout)
##    cout.writeBool(False)
##def recurOpen(item,cin):
##    row,col=cin.readQVariant()
##    canFetch=cin.readBool()
##    if canFetch:
##        item.setRowCount(row)
##        item.setColumnCount(col)
##    while canFetch:
##        ri,ci=cin.readInt32(),cin.readInt32()
##        tmp=QStandardItem()
##        cin>>tmp
##        item.setChild(ri,ci,tmp)
##        recurOpen(tmp,cin)
##        canFetch=cin.readBool()
class StdItemModel(IPickle,QStandardItemModel):
##    def __init__(self,*args):
##        super().__init__(*args)

##    def __iter__(self):
##        self.row_tot=self.rowCount()
##        self.row_cnt=0
        
##        self.col=self.columnCount()
##        self.col_cnt=0
##        return self
    
##    def __next__(self):
##        """返回值按照 [row,col]进位，返回"""
##        if self.col_cnt<self.col:
##            tmp_col=self.col_cnt
##            self.col_cnt+=1
##        else:
##            tmp_col=0
##            self.col_cnt=1
##            self.row_cnt+=1 
##        if self.row_cnt<self.row_tot:
##            tmp_row=self.row_cnt
##        else:
##            raise StopIteration
##        return self.item(tmp_row,tmp_col)
        
    def childs(self):
        rct,cct=self.rowCount(),self.columnCount()
        for r,c in itertools.product(range(rct),range(cct)):
            yield self.item(r,c) 
            
##    def walk(self):
##        for ii in self:
##            if ii:
##                yield ii
##            else:
##                continue
##            for jj in ii.walk():
##                if jj:
##                    yield jj
            
    def __reduce__(self):
        dc={'childs':list(self.childs())}
        
        self.pickleDict.update(dc)                           #新版本的HPickle类的属性
        return super().__reduce__()
    
    def __setstate__(self,state):
        itms=state.pop('childs',None)
        for itm in itms:
            self.setItem(itm.posRow,itm.posCol,itm)
        return super().__setstate__(state)
    
    def remove(self,itm):
        """
        @itm  :  QStandarItem
        该函数采用takeRow的方式，移除item，不会造成Qt删除Internal C++ object，将垃圾回收的工作交给python对象
        """
##        if isinstance(itm, QModelIndex):
##            itm=self.itemFromIndex(itm)
        
        if itm.parent():
            #self.takeRow(itm.row())
            itm.parent().removeRow(itm.row())
        elif itm.model()==self:
            self.removeRow(itm.row())
            
            
    def append(self,data,parent=None):
        '''
        @data   : list[qstanditem] / qstanditem;
        @parent : qstanditem / none
        与Qt的区别是：首先判断data是否存在于model中，如果存在，就先‘移除’它，再在最后append它。
        原装Qt会产生None的项
        '''
        if not parent:
            parent=self
##        else:
##            if isinstance(parent,QModelIndex):#parent是Model index的情况
##                if parent.isValid():
##                    parent=self.itemFromIndex(parent)#.appendRow(data)
##                else:
##                    parent=self
        if isinstance(data,str):
            data=stdItem(data)
        if data.model() is self:
            self.remove(data)
        parent.appendRow(data)
        
##    @adapt(QIODevice.WriteOnly)
##    def save(self,out):
##        "@out: datastream or file name"
##        assert isinstance(out, QDataStream)
##        row,colum=self.rowCount(),self.columnCount()
##        out.writeInt32(row)
##        out.writeInt32(colum)
##        for ri in range(row):
##            for ci in range(colum):
##                if self.index(ri,ci).data():
##                    out.writeBool(True)
##                    out.writeInt32(ri)
##                    out.writeInt32(ci)
##                    out<<self.item(ri,ci)
##        out.writeBool(False)
        
##    @adapt(QIODevice.ReadOnly)
##    def open(self,in_):
##        "@in_: datastream or file name"
##        assert isinstance(in_, QDataStream)
##        row,colum=in_.readInt32(),in_.readInt32()
##        self.setColumnCount(row)
##        self.setRowCount(colum)
##        canFetch=in_.readBool()
##        while canFetch:
##            ri,ci=in_.readInt32(),in_.readInt32()
##            tmp=QStandardItem()
##            in_>>tmp
##            self.setItem(ri,ci,tmp)
##            canFetch=in_.readBool()
    



##class tableModel(mixin,QStandardItemModel):
    pass
##    def __init__(self,parent=None):
##        super().__init__(parent)
##        self.open("d:/tttt.jj")             #  直接从文件恢复

    
##class listModel(mixin,QStandardItemModel):
    """如果不需要太多的功能，可以使用 QStringListModel"""
    pass
##    def __init__(self,parent=None):
##        super().__init__(parent)
##    def append(self,data):
##        """@data ： str,std_itm"""
##        if isinstance(data, QStandardItem):
##            out=data
##        else:
##            out=stdItem(data)
##        self.appendRow(out)
##        return out
        

##    def childrens(self):
##        rows=self.rowCount()
##        ls=[]
##        for ii in xrange(rows):
##            ls.append(self.item(ii))
##        return ls
            
##class treeModel(mixin,QStandardItemModel):
##    def __init__(self,parent=None):
##        super().__init__(parent)


            
##    @adapt(QIODevice.WriteOnly)
##    def save(self,out):
##        '''@type out:str of qdatastream '''
##        row,col=self.rowCount(),self.columnCount()
##        for ri in range(row):
##            for ci in range(col):
##                if self.index(ri,ci).data():
##                    out.writeBool(True)
##                    out.writeInt32(ri)
##                    out.writeInt32(ci)
##                    out<<self.item(ri,ci)
##                    recurSave(self.item(ri,ci), out)
##        out.writeBool(False)
 
##    @adapt(QIODevice.ReadOnly)
##    def open(self,in_):
##        '''@type in_:str or qdatastream '''
##        canFetch=in_.readBool()
##        while canFetch:
##            tmp=QStandardItem()
##            ri,ci=in_.readInt32(),in_.readInt32()
##            in_>>tmp
##            self.setItem(ri,ci,tmp)
##            recurOpen(tmp, in_)
##            canFetch=in_.readBool()
    
##    def headerData(self,sec,orient,role,*args, **kwargs):
##        if orient==Qt.Vertical and role==Qt.DisplayRole:
##            return sec+1
##        return QStandardItemModel.headerData(self, sec,orient,role,*args, **kwargs)
          