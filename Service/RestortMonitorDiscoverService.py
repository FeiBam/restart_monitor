
from Base.Worker import Worker
from utils.Logger import ClassNameLogger, get_class_name_logger


class RestortMonitorDiscoverService(Worker):
    def __init__(self, config, udpClientInstance) -> None:
        super().__init__()
        self.discoverDleay = config.discoverDleay
        self.logger = get_class_name_logger("Server", self.__class__.__name__)
        self.udpClientInstance = udpClientInstance

    def run(self):
        if self.isRunning:
            self.logger.warning("RestortMonitorDiscoverService Alread Running!")
            return False
        self.isRunning = True
        self.thread.run()
        return True

    def stop(self):
        pass

    def loop(self):
        pass