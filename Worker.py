import socket
import codecs
import threading
import logging
from concurrent.futures import ThreadPoolExecutor


class Worker:
    def __init__(self) -> None:
        self.isRunning = False
        self.thread = threading.Thread(target=self.loop)
        self.logger = logging
    
    def run(self):
        if self.isRunning:
            self.logger.warning("Thread Already Running !")
            return
        self.is_running = True
        self.thread.run()
        self.logger.info('Start Runing Worker.')
    
    def stop(self):
        pass

    def loop(self):
        pass