from abc import ABCMeta
import socket
import time

from time import sleep
from Base.Worker import Worker
from utils.Logger import get_class_name_logger
from utils.restart_time_util import calculate_next_restart_time
from Service.UDPService import UDPService
from Base.Event import EventEmitter

from Types.discover_service_event_t import discover_service_event_t
from Types.broadcast_message_t import broadcast_message_t
from Types.discover_service_config_t import discover_service_config_t

import traceback



class DiscoverService(Worker):
    def __init__(self, config: discover_service_config_t, udpServiceInstance: UDPService) -> None:
        super().__init__()
        self.eventEmitter = EventEmitter()
        self.discoverDelay = config.DiscoverDelay
        self.logger = get_class_name_logger("Server", self.__class__.__name__)
        self.udpServiceInstance = udpServiceInstance
        self.SenderPort = config.SenderPort
        self.udpServiceInstance.register_handler(self.handlerMessage)
        self.lastSender = 0

    def sendDiscoverMessage(self):
        address = ("255.255.255.255", self.SenderPort)
        message = bytes([broadcast_message_t.DISCOVER.value])
        self.udpServiceInstance.send_bytes(address, message)

    def sendPingMessage(self):
        address = ("255.255.255.255", self.SenderPort)
        message = bytes([broadcast_message_t.PING.value])
        self.udpServiceInstance.send_bytes(address, message)

    def start(self) -> bool:
        if self.isRunning:
            self.logger.warning("Service Already Running!")
            return False
        self.logger.info("Starting Service")
        self.isRunning = True
        self.logger.info("Start UDPLinster.")
        self.udpServiceInstance.listener()
        self.thread.start()
        self.logger.info("Start Revicer UDP Message.")
        self.udpServiceInstance.start()
        return True

    def stop(self) -> bool:
        if not self.isRunning:
            self.logger.warning("Service Already Stopped!")
            return False
        self.logger.info("Stop Discover Serivice.")
        self.isRunning = False
        self.logger.info("Stop to Revicer UDP Message.")
        self.udpServiceInstance.stop()
        self.executor.shutdown(wait=True)
        self.thread.join()
        self.logger.info("DiscoverService Stopped!")
        return True

    def _loop(self):
        while True:
            if not self.isRunning:
                self.logger.warning("Stop Signal Received, Stopping Thread.")
                return
            try:
                if (time.time() - self.lastSender) > self.discoverDelay:
                    self.logger.debug("Sender Discover Messgae.")
                    self.sendDiscoverMessage()
                    self.lastSender = time.time()
            except Exception as e:
                self.logger.error(f"Error in loop: {e}")
                return e
            finally:
                sleep(1)

    def handlerMessage(self, size: int, data: bytes, addr: tuple):
        data = int.from_bytes(data)
        if data == broadcast_message_t.RECEIVED.value:
            self.eventEmitter.emit(discover_service_event_t.DEVICE_FOUND_NEW.value, size, data, addr)
        if data == broadcast_message_t.PONG.value:
            self.eventEmitter.emit(discover_service_event_t.DEVICE_ALIVE.value, size, data, addr)

    def register_handler(self, event_type: discover_service_event_t, func):
        self.eventEmitter.on(event_type, func)

    @staticmethod
    def build_default_discover_service():
        config = discover_service_config_t(10, 36619, 36618)
        instance = DiscoverService(config)
        return instance