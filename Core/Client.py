import socket
from Base.Worker import Worker
from utils.Logger import ClassNameLogger, get_class_name_logger
from Types.discover_service_config_t import discover_service_config_t as config_t

class RestartMonitorClient(Worker):
    def __init__(self,config : config_t, udpServiceInstance) -> None:
        super.__init__()
        self.udpServiceInstance = udpServiceInstance
        self.LinsterPort = config.listenerPort 
        self.SenderPort =  config.senderPort 
        self.logger = get_class_name_logger("Client",self.__class__.__name__ )

    def handlerRequest(self):
        pass

    def run(self):
        pass

    def stop(self):
        pass

    def loop(self):
        pass
