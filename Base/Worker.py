from abc import ABC, abstractmethod

class Worker(ABC):
    def __init__(self):
        self.is_running = False

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass