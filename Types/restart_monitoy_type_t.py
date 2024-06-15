from dataclasses import dataclass
from enum import Enum, auto

class restart_monitoy_type_t(Enum):
    SERVER = 0x1
    CLIENT = 0x2