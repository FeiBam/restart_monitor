from abc import ABCMeta
import socket

from time import sleep
from Base.Worker import Worker
from Base.Event import EventEmitter
from utils.Logger import get_class_name_logger
from Service.UDPService import UDPService

from Types.broadcast_message_t import broadcast_message_t
from Types.response_service_event_t import response_service_event_t



class ResponseService(Worker):
    def __init__(self, config, max_thread=16):
        super().__init__(max_thread)
        self.listenerPort = config.listenerPort
        self.logger = get_class_name_logger("Server", self.__class__.__name__)
        self.eventEmitter = EventEmitter()
        self.udpServerInstance = UDPService.buildServer(socket.AF_INET, "0.0.0.0", self.listenerPort)
        self.udpClientInstance = UDPService.buildClient(socket.AF_INET, 1)
        self.udpServerInstance.register_handler(self.messageHandler)

    def start(self) -> bool:
        if self.isRunning:
            self.logger.warning("Service Already Running!")
            return False
        self.logger.info("Starting Service")
        self.isRunning = True
        self.thread.start()
        return True
    
    def stop(self) -> bool:
        if not self.isRunning:
            self.logger.warning("Service Already Stopped!")
            return False
        self.isRunning = False
        self.thread.join()
        self.logger.info("Service Stopped!")
        return True
    
    def _loop(self):
        pass

    def response(self, buffer):
        pass

    def handlerMessage(self, data_length, data, address):
        if data == broadcast_message_t.DISCOVER:
            self.eventEmitter.emit(response_service_event_t.RECIVERD_DISCOVER_MESSAGE)

    def register_handler(self, event_type : response_service_event_t, func):
        self.eventEmitter.on(event_type, func)
