from heOs.net_p.server import ServerTcp,erro_rm
from heOs.net_p.client import ClientTcp
import re,socket,select

class HttpProxy:
    def __init__(self,address = ('127.0.0.1',10001),numbers = 10):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.setblocking(False)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR  , 1)
        self.socket.bind(address)
        self.socket.listen(numbers)        
        self.servers=[]
        self.clients = []
        self.maps ={}
##        self.server.readfuncs.append(self.haslink)
    def server_forever(self):
        while 1:
            inputs = [self.socket]+self.servers+ self.clients
            readable , writeable,exp = select.select(inputs,[],inputs)
            for s in readable:
                if s is self.socket:
                    connection , client_add = s.accept()
                    print('<new connecting from> ',client_add)
                    connection.setblocking(False) 
                    self.servers.append(connection)
                else:
                    self.read(s)
                    
    def read(self,sock):
        if sock in self.servers:
            data = sock.recv(4096)
            if data:
                self.haslink(data,sock)
            else:
                sock.close()
                self.servers.remove(sock)
        elif sock in self.clients:
            data = sock.recv(4096)
            if data:
                self.clientrecv(data,sock)
            else:
                sock.close()
                self.clients.remove(sock)  
                del self.maps[sock]
                
    def clientrecv(self,data,sock):
        self.maps[sock].send(data)
    
    def haslink(self,data,sock):
        mt = re.match(b'GET http://([^/\s]+)(/.*)* HTTP',data)
        if mt:
            add = ( mt.group(1).decode('utf8') ,80)
##            self.client.sock.connect( add)
            out = b'GET '+mt.group(2) + data[mt.end():]
            cs = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            #cs.setblocking(False)
            self.maps[cs] = sock
            self.clients.append(cs)
            cs.connect(add)
            cs.send(out)
##            for i in self.client.wait_reply(out):
                
##            while 1:
##                dog1 = self.client.recv(4096)
##                if dog1:
##                    dog+= dog1
##                else:
##                    break
##                sock.send(i)

class Server(ServerTcp):
    def __init__(self,address):
        super().__init__(address)
        self.readfuncs=[]
    @erro_rm
    def read(self,sock):
        data = sock.recv(4096)
##        while 1:
##            data1 = sock.recv(4096)
##            if data1:
##                data += data1
##            else:
##                break
        if not data:
            self.detach(sock)
        else:
            print('[%s]'% str(sock.getpeername() ))
            print(data)   
            for fun in self.readfuncs:
                fun(data,sock)

if __name__ == '__main__':
    prox = HttpProxy()
    prox.server_forever()