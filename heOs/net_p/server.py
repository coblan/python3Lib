#!python3
import select
import socket
import threading

def erro_rm(func):
    def _fun(self,sock,**kw):
        try:
            rt =func(self,sock,**kw)
            return rt
        except ConnectionError as e:
            print(e)
            print(len(self.client) ,'    client remains') 
            self.detach(sock)

    return _fun
            

class ServerTcp:
    def __init__(self,address = ('127.0.0.1',10001),numbers = 10):
        """address:('127.0.0.1',10001)
        numbers: 允许最多多少个连接
        使用select进行轮训，read列表直接使用client，write-check是动态变动的。因为可读的时候，一定会去读，然后清空标志位，
        但是可以写的时候，确不一定写。如果不是动态变动write列表，那么每次轮训都会发回该可写socket，造成调用write函数，造成cpu资源居高不下。
        """
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.setblocking(False)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR  , 1)
        
        self.socket.bind(address)
        self.socket.listen(numbers)
        
        self.client = []
        self.reading =[]
        
        self.client_state = {}
        self.threads = {}
        
    def serve_forever(self):
        print('TCP server starting forever....')
        while True:
            read_chk = [self.socket]
            for i in self.client:
                if i.fileno() == -1:
                    self.detach(i)
                elif i not in self.threads:
                    read_chk.append(i)
##            read_chk = [self.socket]+ self.client
            readable ,writable ,exceptional = select.select(read_chk,[],self.client)
            for s in readable:
                if s is self.socket:
                    connection , client_add = s.accept()
                    print('<new connecting from> ',client_add)
                    connection.setblocking(False)
                    self.attach(connection)
                else:
##                    self.inputs.remove(s)
##                    self.reading.append(s)
##                    thread = threading.Thread(target=self.read,args=(s,))
##                    self.threads[s] = thread
##                    thread.start()
                    
                    self.read(s)
                    
            for s in writable:
                #self.write_chk.remove(s)
                self.write(s)
                
            for s in exceptional:
                self.exceptional(s)
    @erro_rm
    def read(self,sock):
        print('into read')
        data = sock.recv(4096)
        print(repr(data) )
        print(len(data))
        if not data:
            sock.close()
        else:
            print('[%s]'% str(sock.getpeername() ))
            
        #self.client_state[sock] = 'recv'
##        del self.threads[sock]
    @erro_rm  
    def write(self,sock):
        #if self.client_state.get(sock,'') == 'recv':
        sock.send(b'reciev data ----------ok')
        sock.close()
         
    def attach(self,sock):
        self.client.append(sock)
##        self.inputs.append(sock)
##        self.write_chk.append(sock)
        self.client_state[sock] = ''
        
    def detach(self,sock):
        sock.close()
        self.client.remove(sock)
##        if sock in self.write_chk:
##            self.write_chk.remove(sock)
        del self.client_state[sock]
        
    def exceptional(self,sock):
        print(sock.getpeername() ,' has exception')
        sock.close()


class HttpServer(ServerTcp):
    @erro_rm
    def recieved(self,sock):
        data = sock.recv(4960)
        if not data:
            self.detach(sock)
            return
        print('[%s]'%str(sock.getpeername()))
        print(data.decode('utf8'))
        
if __name__ =='__main__':
    test_dog = HttpServer( ('127.0.0.1',10001) )
    test_dog.serve_forever()




