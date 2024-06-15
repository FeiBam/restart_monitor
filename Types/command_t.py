from dataclasses import dataclass
from typing import List, Union, Literal
from enum import Enum, auto
from Types.restart_monitoy_type_t import restart_monitoy_type_t
from Base.Device import Device
from pydantic import BaseModel
from Base.Device import DeviceModel

class command_t(Enum):
    SHOW_DEVICE : int = 0x1
    EXIT : int = 0x2
    INFO : int = 0x3
    RESTART : int = 0x4
    SERVICE_TYPE : int = 0x5
