#! encoding=utf8
from __future__ import unicode_literals
from heQt.qteven import *
from heStruct.pyeven import *
from upload_ui import Ui_Form

class UploadWin(QWidget,Ui_Form):
    def __init__(self,get_metalist, get_metainfo, upload_metainfo, parent=None):
        s(UploadWin,parent)
        self.setupUi(self)
    
        self.get_metalist = get_metalist
        self.get_metainfo = get_metainfo
        self.upload_api = upload_metainfo
        self.setWindowTitle('MetaInfo upload tool')
        self.tableView.setGridStyle(Qt.NoPen)
        self.tableView.setAlternatingRowColors(True)
        self.head = ['Meta ID','App Code','App Name(Production)','Producion Type','App Version','App Store','studio','Status','Approval Status','Approval at']
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(self.head)
        self.tableView.setModel(model)
        self.tableView.viewport().installEventFilter(self)
        
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.btn_get_meta.clicked.connect(self.show_metalist)
        #self.tableView.entered.connect(self.show_metainfo)
        self.btn_upoad_meta.clicked.connect(self.upload_metainfo)
        
    def show_metalist(self):
        self.tableView.model().clear()
        self.tableView.model().setHorizontalHeaderLabels(self.head)
        production_type = self.prodction_type.currentText() if self.prodction_type.currentIndex()>1 else None
        status = self.status.currentText() if self.status.currentIndex()>1 else None
        app_store = self.app_store.currentText() if self.app_store.currentIndex()>1 else None
        studio = self.studio.currentText() if self.studio.currentIndex()>1 else None
        keywords = self.keyword_edit.text()
        datas = self.get_metalist(keywords=keywords, production_type=production_type, status=status, app_store=app_store, studio=studio)
        model = self.tableView.model()
        for i in datas:
            ls = [QStandardItem(j) for j in i]
            model.appendRow(ls)
    
    def show_metainfo(self,index):
        row = index.row()
        self.tableView.selectRow(row)
        metainfo = self.current_metainfo()
        self.textBrowser.clear()
        outstr=''
        for k,v in metainfo.items():
            #self.textBrowser.append('%s\t:%s'%(k,v))
            outstr +=r'<b style="color:red">%s</b><p>%s</p>'%(k,v)
        self.textBrowser.setHtml(outstr)

    def current_metainfo(self):
        index = self.tableView.currentIndex()
        if index.isValid():
            row = index.row()
            model = self.tableView.model()
            meta_id = model.item(row).data(Qt.DisplayRole)
            metainfo = self.get_metainfo(meta_id)    
            return metainfo
        
    def upload_metainfo(self):
        metainfo = self.current_metainfo()
        self.upload_api(metainfo)
        #QMessageBox.information(None,'通知','上传完毕')
        self.msg.setText(u'meta info 上传完成')
        
    def eventFilter(self, obj, event):
        # 点击时，选中一行
        if obj == self.tableView.viewport() and event.type()==QEvent.MouseButtonPress:
            index = self.tableView.indexAt(event.pos())
            if index.isValid():
                self.show_metainfo(index)
            return True
        else:
            #return super().eventFilter(obj,event)
            return s(UploadWin,obj, event)