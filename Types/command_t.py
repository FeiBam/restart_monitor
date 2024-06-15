from dataclasses import dataclass
from typing import List, Union, Literal
from enum import Enum, auto
from Types.restart_monitoy_type_t import restart_monitoy_type_t
from Base.Device import Device
from pydantic import BaseModel
from Base.Device import DeviceModel

class command_t(Enum):
    SHOW_DEVICE = 0x1
    EXIT = 0x2
    INFO = 0x3
    RESTART = 0x4
    SERVICE_TYPE = 0x5




class command_get_server_info_t(BaseModel):
    COMMAND: command_t
    DATA : dict

class command_service_type_t(BaseModel):
    COMMAND : command_t

class command_service_type_reply_t(BaseModel):
    COMMAND: command_t
    DATA: restart_monitoy_type_t

class command_get_devices_t(BaseModel):
    COMMAND : command_t

class command_get_devices_reply_t(BaseModel):
  COMMAND : command_t
  DATA: List[DeviceModel]
  class Config:
        arbitrary_types_allowed = True