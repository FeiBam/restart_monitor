import threading
from concurrent.futures import ThreadPoolExecutor
from abc import ABC, abstractmethod


class Worker(ABC):
    def __init__(self, max_thread=16):
        self.max_thread = max_thread
        self.isRunning = False
        self.thread = threading.Thread(target=self._loop)
        self.executor = ThreadPoolExecutor(max_workers=self.max_thread)

    @abstractmethod
    def start(self) -> bool:
        pass

    @abstractmethod
    def stop(self) -> bool:
        pass

    def _loop(self):
        pass