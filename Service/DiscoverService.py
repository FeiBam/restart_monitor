from abc import ABCMeta
import socket

from time import sleep
from Base.Worker import Worker
from utils.Logger import get_class_name_logger
from Service.UDPService import UDPService
from Base.Event import EventEmitter

from Types.discover_service_event_t import discover_service_event
from Types.broadcast_message_t import broadcast_message
from Types.discover_service_config_t import discover_service_config


class DiscoverService(Worker):
    def __init__(self, config) -> None:
        super().__init__()
        self.eventEmitter = EventEmitter()
        self.remoteDevice = []
        self.discoverDleay = config.discoverDleay
        self.senderPort = config.senderPort
        self.listenerPort = config.listennerPort
        self.logger = get_class_name_logger("Server", self.__class__.__name__)
        #self.udpServerInstance = UDPService.buildServer(socket.AF_INET, "0.0.0.0", self.listenerPort)
        self.udpClientInstance = UDPService.buildClient(socket.AF_INET, 1)
        #self.udpServerInstance.register_handler(self.handlerMessage)
    
    def sendDicoverMessage(self):
        address = ("255.255.255.255", self.senderPort)
        message = bytes([0x1])
        self.udpClientInstance.send_bytes(address, message)

    def start(self):
        if self.isRunning:
            self.logger.warning("Service Alread Running!")
            return False
        self.logger.info("Start Service")
        self.isRunning = True
        self.thread.start()
        return True

    def stop(self):
        if not self.isRunning:
            self.logger.warning("Service Alread Stoped!")
            return
        self.isRunning = False
        self.thread.join()
        self.logger.info("DiscoverService Stoped!")

    def _loop(self):
        while(True):
            if not self.isRunning:
                self.logger.warning("Shutdown Sigle Revicev, Stop Thread.")
                return 
            try:
                self.logger.debug("Sender Discover Message")
                self.sendDicoverMessage()
            except Exception as e:
                self.logger.error(f"Error in loop : {e}")
            finally:
                sleep(self.discoverDleay)
    
    def handlerMessage(self, size, data, addr):
        if data == broadcast_message.PING:
            self.onFoundNewDevice()
    
    def register_handler(self,type : discover_service_event, func):
        self.eventEmitter.on(type, func)

    def onFoundNewDevice(self):
        self.eventEmitter.emit(discover_service_event.DEVICE_FOUND_NEW)

    
