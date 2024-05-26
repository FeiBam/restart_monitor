import socket
import codecs
from Base.Worker import Worker
from utils.Logger import ClassNameLogger,get_class_name_logger


class UDPService(Worker):
    def __init__(self, protocol, addr=None, port=None, max_thread=16):
        super().__init__(max_thread)
        self.addr = addr
        self.port = port
        self.udp_service_type = 0  # default 0, Listener Mode 1, Send Mode 2
        self.handlers = []
        self.socket = socket.socket(protocol, socket.SOCK_DGRAM)
        self.socket.setblocking(False)
        self.logger = get_class_name_logger("Service", self.__class__.__name__)

    def set_service_mode(self, mode):
        self.udp_service_type = mode
    
    def send_bytes(self, addr, buffer):
        if self.udp_service_type == 1:
            self.logger.warning("This instance is in Listener Mode.")
            return
        self.socket.sendto(buffer, addr)

    def send_strings(self, addr, data):
        if self.udp_service_type == 1:
            self.logger.warning("This instance is in Listener Mode.")
            return
        encoded_data = codecs.utf_8_encode(data)[0]
        self.send_bytes(addr, encoded_data)
    
    def listener(self):
        if self.udp_service_type == 1:
            self.logger.warning(f"Already listening on Port: {self.port}")
            return False
        
        if self.udp_service_type == 2:
            self.logger.error("This instance is in Client Mode!")
            return False
        
        self.udp_service_type = 1
        address = ("0.0.0.0", self.port)
        try:
            self.socket.bind(address)
            self.logger.info(f"Start Listener At {address}.")
        except socket.error as e:
            self.udp_service_type = 0
            self.logger.error(f"Failed to bind socket: {e}")
            return False
        return True

    def register_handler(self, func):
        self.handlers.append(func)

    def start(self) -> bool:
        if self.isRunning:
            return False
        self.logger.info("Running UDPService")
        self.isRunning = True
        self.thread.start()
        return True
        
    def stop(self) -> bool:
        if not self.isRunning:
            return False
        self.isRunning = False
        self.socket.close()
        self.executor.shutdown(wait=True)
        self.thread.join()
        self.logger.info("UDPService stopped")
        return True
        
    def _loop(self):
        while True:
            try:
                if not self.isRunning:
                    self.logger.warning("Reciver Stop Sigl Stop Thread.")
                    return
                data, address = self.socket.recvfrom(2048)
                if data:
                    self.logger.debug("Adding task")
                    self.executor.submit(self._handle_data, len(data), data, address)
            except BlockingIOError:
                continue
            

    def _handle_data(self, data_length, data, address):
        for handler in self.handlers:
            try:
                handler(data_length, data, address)
            except Exception as e:
                self.logger.error(f"Error in handler {handler}: {e}")

    def __str__(self):
        return (f"UDPService(addr={self.addr}, port={self.port}, "
                f"udp_service_type={self.udp_service_type}, isRunning={self.isRunning})")

    def __repr__(self):
        return self.__str__()
    
    @staticmethod
    def buildServer(protocol, addr, port, max_thread=16):
        instance = UDPService(protocol, addr, port, max_thread)
        return instance
    
    @staticmethod
    def buildClient(protocol, mode = 0, max_thread=16):
        instance = UDPService(protocol=protocol, max_thread=max_thread)
        instance.set_service_mode(2)
        if mode == 1:
            instance.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        return instance
    

