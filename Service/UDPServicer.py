import socket
import codecs
import logging
import threading
from concurrent.futures import ThreadPoolExecutor

class UDPService:
    def __init__(self, protocol, addr, port, max_thread=16):
        self.addr = addr
        self.port = port
        self.udp_service_type = 0
        self.is_running = False
        self.max_thread = max_thread
        self.handlers = []
        self.executor = ThreadPoolExecutor(max_workers=self.max_thread)
        self.socket = socket.socket(protocol, socket.SOCK_DGRAM)
        self.socket.setblocking(False)
        self.thread = threading.Thread(target=self.loop)
        
    def send_bytes(self, addr, buffer):
        if self.udp_service_type:
            logging.warning("This instance is in Listener Mode.")
            return
        self.socket.sendto(buffer, addr)

    def send_strings(self, addr, data):
        if self.udp_service_type:
            logging.warning("This instance is in Listener Mode.")
            return
        encoded_data = codecs.utf_8_encode(data)[0]
        self.send_bytes(addr, encoded_data)

    def listener(self):
        if self.udp_service_type:
            logging.warning(f"Already listening on Port: {self.port}")
            return
        self.udp_service_type = 1
        address = ("0.0.0.0", self.port)
        self.socket.bind(address)

    def register_handler(self, func):
        self.handlers.append(func)

    def run(self):
        if self.is_running:
            return
        logging.info("Running UDPService")
        self.is_running = True
        self.thread.start()
        
    def stop(self):
        if not self.is_running:
            return
        self.is_running = False
        self.socket.close()
        self.executor.shutdown(wait=True)
        self.thread.join()
        logging.info("UDPService stopped")
        
    def loop(self):
        while True:
            try:
                if not self.is_running:
                    return
                data, address = self.socket.recvfrom(4096)
                if data:
                    logging.debug("Adding task")
                    self.executor.submit(self.handle_data, len(data), data, address)
            except BlockingIOError:
                continue
            except Exception as e:
                logging.error(f"Error in loop: {e}")

    def handle_data(self, data_length, data, address):
        for handler in self.handlers:
            try:
                handler(data_length, data, address)
            except Exception as e:
                logging.error(f"Error in handler {handler}: {e}")
