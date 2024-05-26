import logging

COLOR_CODES = {
    'DEBUG': '\033[36m',    # Cyan
    'INFO': '\033[32m',     # Green
    'WARNING': '\033[33m',  # Yellow
    'ERROR': '\033[31m',    # Red
    'CRITICAL': '\033[41m', # Red background
    'RESET': '\033[0m'      # Reset
}

class ClassNameLogger(logging.Logger):
    def __init__(self, name, class_name, level=logging.NOTSET):
        super().__init__(name, level)
        self.class_name = class_name
        self.add_custom_handler()

    def add_custom_handler(self):
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(color)s [%(levelname)s] %(asctime)s - %(name)s - %(message)s - [%(class_name)s]%(reset)s')
        handler.setFormatter(formatter)
        self.addHandler(handler)

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None, sinfo=None):
        if extra is None:
            extra = {}
        extra['class_name'] = self.class_name
        extra['color'] = COLOR_CODES.get(logging.getLevelName(level), COLOR_CODES['RESET'])
        extra['reset'] = COLOR_CODES['RESET']
        return super().makeRecord(name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)

def get_class_name_logger(name, class_name, level=logging.DEBUG):
    logging.setLoggerClass(ClassNameLogger)
    logger = ClassNameLogger(name, class_name, level)
    logging.setLoggerClass(logging.Logger)  # Reset to default to avoid affecting other loggers
    return logger