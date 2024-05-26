import socket
import time
from Base.Worker import Worker
from utils.Logger import get_class_name_logger


class RestartMonitorServer(Worker):
    def __init__(self, config, UDPService) -> None:
        super.__init__()
        self.UDPService = UDPService
        self.UDPServer = UDPService(socket.AF_INET,"0.0.0.0")
        self.UDPClient = UDPService(socket.AF_INET,"0.0.0.0")
        self.Clients = []
        self.logger = get_class_name_logger("Server", self.__class__.__name__)
        self.listenerPort = config.listennerPort
        self.senderPort = config.senderPort

    def handlerRequest(self, data, address):
        pass
    
    def getClients(self):
        return self.Clients

    def discoverClient(self):
        message = 0x1
        address = ("<broadcast>",self.senderPort)
        self.UDPClient.send_bytes(address, message)

    def addClient(self):
        pass

    def UpdateClients(self):
        pass

    def run(self):
        if self.is_running:
            self.logger.warning("Server Already Runnning!")
            return False
        self.isRunning = True
        self.thread.run()
        return True

    def stop(self):
        if not self.is_running:
            self.logger.warning("Server Already Stoped!")
            return False
        self.isRunning = False
    
    def loop(self):
        while(True):
            if not self.isRunning:
                self.logger.info("Server Stop Running!")
                return
            


        

        
            
            

