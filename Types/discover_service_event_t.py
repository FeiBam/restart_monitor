from enum import Enum, auto

class discover_service_event(Enum):
    DEVICE_FOUND_NEW = auto()
    DEVICE_OFFLINE = auto()
    DEVICE_REPLY = auto()



