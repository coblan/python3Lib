from PyQt5.QtNetwork import *
from PyQt5.QtCore import *
import sys,re

class Proxy(QObject):
    def __init__(self,*args):
        super().__init__(*args)
        self.sever = QTcpServer()
        self.sever.listen(QHostAddress.Any,10001)
        print('proxy is listion ...')
        self.conns = []
        self.maps={}
        self.sever.newConnection.connect(self.on_newcon)
        
    def on_newcon(self):
        con = self.sever.nextPendingConnection()
        self.conns.append(con)
        con.readyRead.connect(self.readyRead)
    def readyRead(self):
        text = self.sender().readAll().data()
        print(text)
        
        self.haslink(text,self.sender())
    
    def haslink(self,data,sock):
        mt = re.match(b'GET http://([^/\s]+)(/.*)* HTTP',data)
        if mt:
            add =  mt.group(1).decode('utf8') 
            out = b'GET '+mt.group(2) + b' HTTP'+data[mt.end():]            
            cs = QTcpSocket(self)
            cs.out = out
            cs.server = sock
            cs.connectToHost(add,80)
            cs.connected.connect(self.connect_client)            
            
            
            
    def connect_client(self):
        cs = self.sender()
        cs.readyRead.connect(self.client_ready)
        cs.write(cs.out)   
    def client_ready(self):
        qbyte = self.sender().readAll()
##        print('recv')
##        print(qbyte.data())
        self.sender().server.write(qbyte.data())
if __name__ == '__main__':
    app = QCoreApplication(sys.argv)
    pro = Proxy()
##    pro.sever.listen(
    sys.exit(app.exec_())