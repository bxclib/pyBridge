import socketserver
import sys
import time
BUF_SIZE=512
ACK="ack"
ARD="ard"
INTERVAL=3
    
class Bridge_server(socketserver.BaseRequestHandler):
    def handle(self):
        print ("Connecting with {} {}:".format(self.client_address[0],self.client_address[1]))
        self.execlist=[]
        try:
            while True:                
                # self.request is the TCP socket connected to the client
                self.data = self.request.recv(BUF_SIZE).decode("utf-8").strip()
                if self.data=="":
                    time.sleep(INTERVAL)
                    continue
                print ("Receiving package")
                size=int(self.data)
                #print (size)
                self.request.send(ACK.encode("utf-8"))
                if size>0:
                    print ("Package size is",size)
                    self.data=self.request.recv(size).strip()
                    cmd=self.data.decode("utf-8")
                    self.request.send(ARD.encode("utf-8"))
                    self.process_cmd(cmd)
                if  size<0:
                    print ("Package size is",-size)
                    self.data=self.request.recv(-1*size).strip()
                    self.request.send(ARD.encode("utf-8"))
                    self.process_data(self.data)
        except:
            print("Unexpected error:", sys.exc_info())
            self.error(1)
    def error(self,code):
        if code==1:
            print ("There is a error during handling the package.")
    def process_cmd(self,cmd):
        #print ("processing cmd -->",cmd)
        if cmd=="end":
            print ("Begin to execute")
        else:
            self.execlist.append(('c',cmd))
        print (self.execlist)
    def process_data(self,data):
        #print ("processing data")
        #print (data)
        self.execlist.append(('d',data))
        print (self.execlist)
if __name__ == "__main__":
    
    HOST, PORT = "localhost", 9999

    # instantiate the server, and bind to localhost on port 9999
    server = socketserver.ThreadingTCPServer((HOST, PORT), Bridge_server)
    # activate the server
    # this will keep running until Ctrl-C
    server.serve_forever()
    
