import socket
from Worker import Worker
from Logger import ClassNameLogger, get_class_name_logger




class RestartMonitorClient(Worker):
    def __init__(self,config,UDPService) -> None:
        super.__init__()
        self.UDPService = UDPService
        self.UDPServer = UDPService(socket.AF_INET, "0.0.0.0")
        self.UDPClient = UDPService(socket.AF_INET, "0.0.0.0")
        self.logger = get_class_name_logger("Client",self.__class__.__name__ )

    def handlerRequest(self):
        pass

    def run(self):
        pass

    def stop(self):
        pass

    def loop(self):
        pass