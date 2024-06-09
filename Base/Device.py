import time
from Base.Worker import Worker
import threading

class Device(Worker):
    def __init__(self, udp_service, address, timeout=5):
        super().__init__(max_thread=1)  # Device 只需要一个线程来管理其状态
        self.udp_service = udp_service
        self.address = address
        self.status = "OFFLINE"
        self.last_response_time = None
        self.timeout = timeout
        self.lock = threading.Lock()

    def get_status(self):
        self.udp_service.send_strings(self.address, "Status request")
        with self.lock:
            self.last_response_time = time.time()

    def handle_response(self, data_length, data, address):
        if address == self.address:
            with self.lock:
                self.status = "ONLINE"
                self.last_response_time = time.time()

    def check_timeout(self):
        with self.lock:
            if self.last_response_time and (time.time() - self.last_response_time > self.timeout):
                self.status = "OFFLINE"

    def start(self) -> bool:
        if self.isRunning:
            return False
        self.isRunning = True
        self.thread.start()
        return True 

    def stop(self) -> bool:
        if not self.isRunning:
            return False
        self.isRunning = False
        self.thread.join()
        return True

    def _loop(self):
        while self.isRunning:
            self.get_status()
            time.sleep(self.timeout)
            self.check_timeout()

    def __str__(self):
        return f"Device(address={self.address}, status={self.status})"

    def __repr__(self):
        return self.__str__()