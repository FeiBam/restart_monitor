from enum import Enum, auto

class discover_service_event_t(Enum):
    DEVICE_FOUND_NEW = auto()
    DEVICE_OFFLINE = auto()
    DEVICE_REPLY = auto()
    DEVICE_ALIVE = auto()




