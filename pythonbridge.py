import socket
import sys
BUF_SIZE=512
ACK="ack"
ARD="ard"
class Bridge():
    def __init__(self,addr):
        self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)     
        self.s.connect(addr)
    def send_cmd(self,cmd):
        self.s.send(str(sys.getsizeof(cmd)).encode('utf-8'))      
        a=self.s.recv(BUF_SIZE).decode("utf-8").strip()    
        if a==ACK:
            self.s.send(cmd.encode('utf-8'))
            a=self.s.recv(BUF_SIZE).decode("utf-8").strip()
            if a==ARD:
                return 0
            else:
                print ("ARD error when sending command",a)
                return 1
        else:
            print ("ACK error when sending command",a)
            return 1
    def send_data(self,data):
        self.s.send(str(-1*sys.getsizeof(data)).encode('utf-8')) 
        a=self.s.recv(BUF_SIZE).decode("utf-8").strip()    
        if a==ACK:
            self.s.send(data)
            a=self.s.recv(BUF_SIZE).decode("utf-8").strip()
            if a==ARD:
                return 0
            else:
                print ("ARD error when sending data",a)
                return 1
        else:
            print ("ACK error when sending data",a)
            return 1
    def close(self):
        self.s.close()
HOST='localhost'
PORT=9999
pybridge=Bridge((HOST,PORT))
#s.send("50".encode("utf-8"))
pybridge.send_cmd("start")
pybridge.send_cmd("pipe build")
pybridge.send_cmd("pipe open --mode=t")
pybridge.send_data((5).to_bytes(10, byteorder='big'))
pybridge.send_data((5).to_bytes(1, byteorder='big'))
pybridge.send_data((5).to_bytes(10, byteorder='big'))
pybridge.send_cmd("end")
pybridge.close() 
