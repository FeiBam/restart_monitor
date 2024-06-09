import threading
import time
from utils.Logger import get_class_name_logger
from Base.Device import Device
from Base.Worker import Worker

class DeviceManager(Worker):
    def __init__(self, udp_service, status_check_interval=10):
        super().__init__()
        self.udp_service = udp_service
        self.devices = {}
        self.status_check_interval = status_check_interval
        self.logger = get_class_name_logger("Service", self.__class__.__name__)

    def add_device(self, address, timeout=5):
        device = Device(self.udp_service, address, timeout)
        self.devices[address] = device
        self.udp_service.register_handler(device.handle_response)
        self.logger.info(f"Added device {address}")
        device.start()  # 启动设备监控

    def start(self) -> bool:
        if self.isRunning:
            return False
        self.isRunning = True
        self.thread.start()
        return True
    
    def getDevices(self):
        return self.devices

    def stop(self) -> bool:
        if not self.isRunning:
            return False
        self.isRunning = False
        for device in self.devices.values():
            device.stop()
        self.thread.join()
        return True

    def _loop(self):
        while self.isRunning:
            for device in self.devices.values():
                self.logger.info(str(device))
            time.sleep(self.status_check_interval)

    def __str__(self):
        return f"DeviceManager(devices={self.devices})"

    def __repr__(self):
        return self.__str__()