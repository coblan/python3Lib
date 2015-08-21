# -*- encoding:utf8 -*-

from PySide.QtGui import * 
from PySide.QtCore import *

from heOs.pickle_ import IPickle
import pickle,itertools
class StdItem(IPickle, QStandardItem):
    """
*. 实现了pickle支持.利用的是Qt的QDatastream来pickle了Item，所以你需要遵守QStandardItem存储数据的规则。
   例如，item.setdata(Qt.userRole+1,someObj)
   如果要使用python的item.propery的方式保存数据，必须更新item.pickleDict


*.  迭代:迭代直接儿子项
    walk:迭代所有后代项
    
    修改了remove的C++行为，不在由C++删除remove的项
    修改了append的C++行为，如果std_item的后代项中已经包括了简要append的项，那么将该项移到最后。
    """
##    def __init__(self, *args):
##        super().__init__(*args)
        
##    def __iter__(self):
##        self.row_tot = self.rowCount()
##        self.row_crt = 0
        
##        self.col = self.columnCount()
##        self.col_cnt = 0
##        self.init_iter=True
##        return self 
    
##    def __next__(self):
##        """返回值按照 [row,col]进位，返回"""
##        if self.init_iter:
##            self.init_iter=False
##            return self
        
##        if self.col_cnt<self.col:
##            tmp_col = self.col_cnt
##            self.col_cnt += 1
##        else:
##            tmp_col = 0
##            self.col_cnt = 1
##            self.row_crt += 1 
##        if self.row_crt < self.row_tot:
##            tmp_row = self.row_crt
##        else:
##            raise StopIteration
##        return self.child(tmp_row,tmp_col)
    def childs(self):
        rct,cct=self.rowCount(),self.columnCount()
        for r,c in itertools.product(range(rct),range(cct)):
            yield self.child(r,c)
            
    def walk(self):
        yield (self, self.childs())
        for jj in list(self.childs()):
            for f in  jj.walk():
                yield f
                
            
    def __reduce__(self):
        """
        请使用pickle_dict属性来限定需要pickle的内容
        """
        buf = QByteArray()
        out = QDataStream(buf,QIODevice.WriteOnly)
        out << self
        self.posRow = self.row()
        self.posCol = self.column()
        dc = {'qbyte' : buf,
              'posRow' : self.posRow,
              'posCol' : self.posCol, 
              "childs": pickle.dumps (list(self.childs()) ),}
        
        #如果是treeView，有可能会要求保留expand状态
        if hasattr( self.model(),'treeView'):
            dc['expand'] = self.model().treeView.isExpanded(self.index())
            dc['selected']= self.model().treeView.currentIndex()==self.index()
          
        self.pickleDict.update(dc)                # 由于qt很多元素都不能pickle，所以最好用pickle_dict来限制需要pickle的元素
        return super(StdItem,self).__reduce__()
    
    def __setstate__(self,state):
        """
        state是一个字典，state['qbyte']是buf数据
        """
        buf = state.pop('qbyte')
        in_ = QDataStream(buf,QIODevice.ReadOnly)
        in_ >> self
        
        childByt = state.pop("childs", None)
        if childByt:
            childs = pickle.loads(childByt )
            for child in childs:
                self.append(child)
            
        return super(StdItem,self).__setstate__(state)
    
    #def next_sib(self):
        #p=self.parent()
        #if p:
            #if p.rowCount()>self.row():
                #return p.child(self.row()+1)
        #else:
            #mode=self.model()
            #if mode.rowCount()>self.row():
                #return mode.item(self.row()+1)
    
##    def parents(self):
##        p=self.parent()
##        if p:
##            yield p
##            if isinstance(p,std_item):
##                for ii in p.parents():
##                    yield ii
    
    def remove(self,data):
        """
        @data : QstandardItem
        修改了remove的C++行为，不在由C++删除remove的项"""
        if data in self.childs():
            self.takeRow(data.row())
        
    def append(self,data, checkIfExist = False):
        """
        checkIfExist = True
        修改了append的C++行为，如果std_item的 孩子 项中已经包括了将要append的项，那么将该项移到最后。
        """
        if checkIfExist:
            for ii in self.walk():
                if ii is data:
                    self.remove(ii)
                    break
        if isinstance(data,str):
            data=StdItem(data)
        self.appendRow(data)
    
    def __hash__(self):
        return id(self)
        
if __name__=='__main__':
    import pickle,sys
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *
    
    from heQt.itemModel import StdItemModel
    app=QApplication(sys.argv)
    jj=StdItem()
    #jj=QStandardItem()
    jj.setData('haha',Qt.UserRole+1)

    mode=StdItemModel()
    #mode=QStandardItemModel()
    mode.append(jj)
    st= pickle.dumps(jj)
    kk=pickle.loads(st)
    
    mode.appendRow(kk)
    mode.appendRow(pickle.loads(st))
    hm1=pickle.dumps(mode)
    
    hm2=pickle.loads(hm1)
    print(hm2)
    sys.exit(app.exec_())