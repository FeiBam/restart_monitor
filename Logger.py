import logging

class ClassNameLogger(logging.Logger):
    def __init__(self, name, class_name, level=logging.NOTSET):
        super().__init__(name, level)
        self.class_name = class_name
        self.add_custom_handler()

    def add_custom_handler(self):
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(class_name)s]')
        handler.setFormatter(formatter)
        self.addHandler(handler)

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None, sinfo=None):
        if extra is None:
            extra = {}
        extra['class_name'] = self.class_name
        return super().makeRecord(name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)

def get_class_name_logger(name, class_name, level=logging.DEBUG):
    logging.setLoggerClass(ClassNameLogger)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.class_name = class_name
    return logger
