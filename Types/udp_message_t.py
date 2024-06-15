
from dataclasses import dataclass
from Types.discover_service_config_t import discover_service_config_t
from Types.restart_time_setting_t import restart_time_setting_t
from Types.command_t import *
from pydantic import BaseModel
from typing import Union, Literal
from enum import Enum, auto

class message_type_t(Enum):
    COMMAND = 0x1
    MESSAGE = 0x2


class udp_message_t(BaseModel):
    MESSAGE_TYPE: message_type_t
    PAYLOAD: Union[command_service_type_t, command_get_devices_reply_t, command_get_server_info_t, command_get_devices_reply_t, command_get_server_info_t]





