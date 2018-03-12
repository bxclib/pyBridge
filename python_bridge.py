import socket
import sys
BUF_SIZE=512
ACK="ack"
ARD="ard"
def send_cmd(s,cmd):
    s.send(str(sys.getsizeof(cmd)).encode('utf-8'))      
    a=s.recv(BUF_SIZE).decode("utf-8").strip()    
    if a==ACK:
        s.send(cmd.encode('utf-8'))
        a=s.recv(BUF_SIZE).decode("utf-8").strip()
        if a==ARD:
            return 0
        else:
            print ("ard",a)
            return 1
    else:
        print ("ack",a)
        return 1
def send_data(s,data):
    s.send(str(-1*sys.getsizeof(data)).encode('utf-8')) 
    a=s.recv(BUF_SIZE).decode("utf-8").strip()    
    if a==ACK:
        s.send(data)
        a=s.recv(BUF_SIZE).decode("utf-8").strip()
        if a==ARD:
            return 0
        else:
            print ("ard",a)
            return 1
    else:
        print ("ack",a)
        return 1
    
HOST='localhost'
PORT=9999
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)     
s.connect((HOST,PORT))
#s.send("50".encode("utf-8"))
#send_cmd(s,"pipe open")
#send_data(s,(5).to_bytes(10, byteorder='big'))
#send_data(s,(5).to_bytes(1, byteorder='big'))
#send_data(s,(5).to_bytes(10, byteorder='big'))
#send_cmd(s,"end")
#s.close()   #关闭连接
