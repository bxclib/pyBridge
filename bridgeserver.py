import socketserver
import sys
import time
import execcmd
BUF_SIZE=512
ACK="ack"
ARD="ard"
INTERVAL=3
    
class BridgeServer(socketserver.BaseRequestHandler):
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
                #print ("Receiving package")
                size=int(self.data)
                #print (size)
                self.request.send(ACK.encode("utf-8"))
                if size>0:
                    #print ("Package size is",size)
                    self.data=self.request.recv(size).strip()
                    cmd=self.data.decode("utf-8")
                    self.request.send(ARD.encode("utf-8"))
                    self.process_cmd(cmd)
                if  size<0:
                    #print ("Package size is",-size)
                    self.data=self.request.recv(-1*size).strip()
                    self.request.send(ARD.encode("utf-8"))
                    self.process_data(self.data)
        except:
            print("Unexpected error:", sys.exc_info())
    def process_cmd(self,cmd):
        #print ("processing cmd -->",cmd)
        if cmd=="end":
            self.execlist.append(('c',cmd))
            #print ("Begin to execute")
            self.exec_cmdlist()
        else:
            self.execlist.append(('c',cmd))
        #print (self.execlist)
    def process_data(self,data):
        #print ("processing data")
        #print (data)
        self.execlist.append(('d',data))
        #print (self.execlist)
    def exec_cmdlist(self):
        while self.execlist!=[]:
            self.parse(self.execlist[0][1])
            #print (self.execlist)
    def parse(self,cmd):
        cmd_dict={}
        cmd=cmd.split(" ")
        cmd_dict["base_cmd"]=cmd[0]
        if cmd[0]!='start' and cmd[0]!='end':
            cmd_dict["cmd"]=cmd[1]
            cmd_dict["options"]=[]
            if len(cmd)>2:
                for option in cmd[2:]:
                    option=option.split("=")
                    option=(option[0][2:],option[1])
                    cmd_dict["options"].append(option)
            del (self.execlist[0])
            cmd_dict["data"]=[]
            while self.execlist[0][0]=='d':
                cmd_dict["data"].append(self.execlist[0][1])
                del (self.execlist[0])
        else:
            cmd_dict["cmd"]=""
            cmd_dict["options"]=[]
            cmd_dict["data"]=[]
            del (self.execlist[0])
        self.exec(cmd_dict)    
    def exec(self,cmd_dict):
        execcmd.ExecCmd(cmd_dict)
if __name__ == "__main__":
    
    HOST, PORT = "localhost", 9999

    # instantiate the server, and bind to localhost on port 9999
    server = socketserver.ThreadingTCPServer((HOST, PORT), BridgeServer)
    # activate the server
    # this will keep running until Ctrl-C
    server.serve_forever()
    
