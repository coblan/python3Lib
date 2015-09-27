import socket,select

class ClientTcp:
    def __init__(self,address = None):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        if address:
            self.sock.connect(address)
    
##    def wait_reply(self,byt):
##        self.sock.send(byt)
##        while 1:
##            if self.sock.fileno()== -1:
##                print('clent quit')
##                return
##            readable ,_,_ = select.select([self.sock],[],[])
##            for i in readable:
##                data = i.recv(4960)
##                if data:
##                    yield data
##                else:
##                    return
        
    
    def send(self,byt):
        self.sock.send(byt)

if __name__ == '__main__':
    c1= ClientTcp(('127.0.0.1',10001))
    c1.send(b'ok')


