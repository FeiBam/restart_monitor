from enum import Enum, auto

class broadcast_message_t(Enum):
    PING = 0x1
    PONG = 0X2
    DISCOVER = 0x3
    RECEIVED = 0x5
    STATUS = 0X4