#!python3

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from heOs.pickle_ import IPickle
import pickle,itertools



class StdItem(QStandardItem):
    """
    通过直接修改QStandardItem，增加pickle功能，childs,walk遍历功能
    
*. 实现了pickle支持.利用的是Qt的QDatastream来pickle了Item，所以你需要遵守QStandardItem存储数据的规则。
   例如，item.setdata(Qt.userRole+1,someObj)
   如果要使用python的item.propery的方式保存数据，必须更新item.pickle_dict


*.  迭代:迭代直接儿子项
    walk:迭代所有后代项
    
    X 修改了remove的C++行为，不在由C++删除remove的项
    X 修改了append的C++行为，如果std_item的后代项中已经包括了简要append的项，那么将该项移到最后。
    """
    #def __init__(self, item=None):
        #super().__init__()
        #if isinstance( item,QStandardItem):
            #self.item = item
        #elif isinstance(item,str):
            #self.item = QStandardItem(item)
        #else:
            #self.item = QStandardItem()
            
    #def __getattr__(self,name):
        #return getattr(self.item,name)

    def childs(self):
        rct,cct=self.rowCount(),self.columnCount()
        for r,c in itertools.product(range(rct),range(cct)):
            yield  self.child(r,c)
            
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

        dc = {'p_qbyte' : buf,
              'p_posRow' : self.row(),
              'p_posCol' : self.column(), 
              "p_childs": list(self.childs()),}
        
        #如果是treeView，有可能会要求保留expand状态
        if hasattr( self.model(),'treeView'):
            dc['p_expand'] = self.model().treeView.isExpanded(self.index())
            dc['p_selected']= self.model().treeView.currentIndex()==self.index()
            
        if hasattr(self,'pickle_dict'):
            self.pickle_dict.update(dc)                # 由于qt很多元素都不能pickle，所以最好用pickle_dict来限制需要pickle的元素
        else:
            self.pickle_dict = dc
        return self.__class__,(),self.pickle_dict
    
    def __setstate__(self,state):
        """
        state是一个字典，state['qbyte']是buf数据
        """
        buf = state.pop('p_qbyte')
        in_ = QDataStream(buf,QIODevice.ReadOnly)
        in_ >> self
        
        childs = state.pop("p_childs", None)
        self.__dict__.update(state)
        
        for child in childs:
            self.setChild(child.p_posRow,child.p_posCol,child)
        
        
    
    
    def remove(self,data):
        """
        @data : QstandardItem
        修改了remove的C++行为，不在由C++删除remove的项"""
        if data in self.childs():
            self.takeRow(data.row())
        
    #def append(self,data, checkIfExist = False):
        #"""
        #checkIfExist = True
        #修改了append的C++行为，如果std_item的 孩子 项中已经包括了将要append的项，那么将该项移到最后。
        #"""
        #if checkIfExist:
            #for ii in self.walk():
                #if ii is data:
                    #self.remove(ii)
                    #break
        #if isinstance(data,str):
            #data=QStandardItem(data)
        #elif isinstance(data,StdItem):
            #data=data.item
        #self.appendRow(data)
    
    def __hash__(self):
        return id(self)

for k,v in StdItem.__dict__.items():
    setattr(QStandardItem,k,v)

if __name__=='__main__':
    import pickle,sys
##    from heQt.item import StdItem
##    from heQt.itemModel import StdItemModel
    app=QApplication(sys.argv)
    
##    jj=StdItem(QStandardItem() )
    jj=QStandardItem()
    jj.setData('haha',Qt.UserRole+1)

##    mode=StdItemModel()
    mode=QStandardItemModel()
##    mode.append(jj)
    st= pickle.dumps(jj)
    kk=pickle.loads(st)
    print(st)
    print(kk)
##    mode.appendRow(kk.item)
##    print(kk.data())
##    mode.appendRow(pickle.loads(st).item)
##    hm1=pickle.dumps(mode)
    
##    hm2=pickle.loads(hm1)
##    print(hm2)
    

    sys.exit(app.exec_())