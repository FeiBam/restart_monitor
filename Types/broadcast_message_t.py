from enum import Enum, auto

class broadcast_message(Enum):
    PING = 0x1
    PONG = 0X2
    DISCOVER = 0x3