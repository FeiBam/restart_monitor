from Base.Worker import Worker
from Service.UDPService import UDPService
from utils.Logger import ClassNameLogger, get_class_name_logger
from Types.client_config_t import client_config_t
from Types.broadcast_message_t import broadcast_message_t
from Types.discover_service_event_t import discover_service_event_t
from Types.udp_callback_interface_t import udp_callback_interface_t


class RestartMonitorClient(Worker):
    def __init__(self,config : client_config_t, udpServiceInstance :UDPService) -> None:
        super.__init__()
        self.max_thread = 0
        self.udpServiceInstance = udpServiceInstance
        self.udpServiceInstance.register_handler(self.handlerDISCOVERMessage)
        self.LinsterPort = config.ListenerPort
        self.SenderPort =  config.SenderPort
        self.logger = get_class_name_logger("Client", self.__class__.__name__ )

    def handlerUDPMessage(self, data_length: int, data: bytes, address: tuple): 
        data = int.from_bytes(data)
        if data == broadcast_message_t.DISCOVER.value:
            addr = (address[0], self.SenderPort)
            message = broadcast_message_t.RECEIVED.value
            self.udpServiceInstance.send_strings(addr, message)

        if data == broadcast_message_t.PING.value:
            addr = (address[0], self.SenderPort)
            message = broadcast_message_t.PONG.value
            self.udpServiceInstance.send_strings(addr, message)

    def start(self) -> bool:
        if self.isRunning:
            self.logger.warn("Client Background Service Already Running!")
            return False
        self.logger.info("Start UDPService.")
        self.udpServiceInstance.listener()
        self.udpServiceInstance.start()
        self.logger.info("UDPService Started.")
        self.logger.info("Start Client Background Service.")
        self.isRunning = True
        self.logger.info("Client Background Service Start Success !")
        return True

    def stop(self) -> bool:
        if not self.isRunning:
            self.logger.warn("Client Background Service Alread Stoped!")
            return False
        self.logger.info("Stop Reciver UDPMessage.")
        self.udpServiceInstance.stop()
        self.logger.info("Stop Client Background Service.")
        self.isRunning = False
        self.logger.info("Client Background Service Stoped!")
        return True

    def _loop(self):
        pass
