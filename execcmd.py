class ExecCmd():
    def __init__(self,cmd_dict):
        eval("self."+cmd_dict["base_cmd"]+"(cmd_dict)")
    def start(self,cmd_dict):
        print ("start")
        pass
    def end(self,cmd_dict):
        print ("end")
        pass
    def pipe(self,cmd_dict):
        def build(cmd_dict):
            print ("pipe build")
            print (cmd_dict)
        def open(cmd_dict):
            print ("pipe open")
            print (cmd_dict)
        eval(cmd_dict["cmd"]+"(cmd_dict)")
    

