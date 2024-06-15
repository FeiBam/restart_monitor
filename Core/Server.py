import time
import json
import os
from utils.JsonSerializable import JsonSerializable
from concurrent.futures import ThreadPoolExecutor
from Base.Worker import Worker
from utils.Logger import get_class_name_logger
from Service.DiscoverService import DiscoverService
from Types.discover_service_event_t import discover_service_event_t
from Types.server_config_t import server_config_t
from datetime import datetime
from Base.Device import Device
from utils.restart_time_util import calculate_next_restart_time


class RestartMonitorServer(Worker):
    def __init__(self, config: server_config_t, udpServiceInstance) -> None:
        super().__init__()
        self.udpServiceInstance = udpServiceInstance
        self.discoverService = DiscoverService(config.DiscoverConfig, udpServiceInstance)
        self.discoverService.register_handler(discover_service_event_t.DEVICE_FOUND_NEW.value, self.addClient)
        self.discoverService.register_handler(discover_service_event_t.DEVICE_REPLY.value, self.onDeviceReply)
        self.logger = get_class_name_logger("RestartMonitorServer", __class__.__name__)
        self.isDelay = False
        self.Devices : Device = [] 
        self.config = config
        self.nextRestartTime = calculate_next_restart_time(config.RestartAT)
        self.lastCheckAt = 0
        self.nowTime = time.time()
        self.isRunning = False
        self.restart_info = {'lastRestartAt': None , "nextRestartTime" : self.nextRestartTime}

    def addClient(self, size: int, data: bytes, addr: tuple):
        device = Device(None, addr, 25)
        device.last_response_time = time.time()
        device.status = "ONLINE"
        self.Devices.append(device)
        self.logger.info(f"Added new device: {addr}")

    def updateClients(self):
        current_time = time.time()
        for device in list(self.Devices):
            if current_time - device.last_response_time > self.config.DeviceTimeOut:
                self.logger.info(f"Device {device.address} timed out, removing from list.")
                self.Devices.remove(device)

    def onDeviceReply(self, size: int, data: bytes, addr: tuple):
        for device in self.Devices:
            if device.addr == addr:
                device.last_response_time = time.time()
                self.logger.info(f"Received reply from device: {addr}")

    def start(self) -> bool:
        if self.isRunning:
            self.logger.warning("Server already running!")
            return False
        self.isRunning = True
        self.logger.info("Starting Discover Service.")
        self.discoverService.start()
        self.logger.info("Starting Server Main Loop.")
        self.thread.start()
        return True

    def stop(self) -> bool:
        if not self.isRunning:
            self.logger.warning("Server already stopped!")
            return False
        self.isRunning = False
        self.executor.shutdown(wait=True)
        self.thread.join()
        self.discoverService.stop()
        self.logger.info("Server stopped!")
        return True
    
    def restart(self):
        self.restart_info["lastRestartAt"] = self.nowTime
        with open("cache.json", "w") as json_file:
            json.dump(self.restart_info, json_file, indent=4)
        self.logger.info("Restarting system...")
        if os.name == 'nt':  # Windows
            self.logger.info("is windows! shutdown /r /t 1")
            #os.system("shutdown /r /t 1")
        else:  # Linux and other Unix-like systems
            self.logger.info("is linux! sudo reboot!")
            #os.system("sudo reboot")

    def _loop(self):
        while True:
            if not self.isRunning:
                self.logger.warn("Stop Signal Received, Stopping Thread.")
                return
            self.nowTime = time.time()
            if self.lastCheckAt + self.config.DeviceUpdateDelay < self.nowTime:
                self.logger.info("Check Device Status, Send Ping Message.")
                self.discoverService.sendPingMessage()
                self.logger.info("Update Client list.")
                self.updateClients()
                self.lastCheckAt = time.time()
            if self.nextRestartTime < self.nowTime:
                self.logger.info("It's time to try restart...")
                if len(self.Devices) > 0:
                    self.logger.info("Have Remote device online, delaying restart...")
                    self.nextRestartTime += self.config.delay
                    continue
                restart_time = datetime.fromtimestamp(self.nowTime + 60).strftime('%Y-%m-%d %H:%M:%S')
                self.logger.info(f"Will restart at {restart_time}.")
                self.restart()
            else:
                self.logger.debug("Not time yet, waiting...")
            time.sleep(1)  # 添加睡眠以防止高 CPU 占用