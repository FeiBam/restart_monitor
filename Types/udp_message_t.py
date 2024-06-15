
from dataclasses import dataclass
from Types.discover_service_config_t import discover_service_config_t
from Types.restart_time_setting_t import restart_time_setting_t
from Types.command_t import *
from pydantic import BaseModel , Field
from typing_extensions import Annotated
from typing import Union, Literal
from enum import Enum, auto

class message_type_t(Enum):
    COMMAND : int = 0x1
    MESSAGE : int = 0x2


class udp_message_command_get_service_type_payload_t(BaseModel):
    COMMAND :  command_t

class udp_message_command_get_service_type_t(BaseModel):
    MESSAGE_TYPE : message_type_t
    PAYLOAD : udp_message_command_get_service_type_payload_t

class udp_message_command_get_service_type_reply_payload_t(BaseModel):
    COMMAND : command_t
    DATA : restart_monitoy_type_t

class udp_message_command_get_service_type_reply_t(BaseModel):
    MESSAGE_TYPE : message_type_t
    PAYLOAD : udp_message_command_get_service_type_reply_payload_t

class udp_message_command_get_server_info_reply_payload_t(BaseModel):
    COMMAND : command_t
    DATA : restart_monitoy_type_t

class udp_message_command_get_server_info_payload_t(BaseModel):
    COMMAND : command_t

class udp_message_command_get_server_info_t(BaseModel):
    MESSAGE_TYPE : message_type_t
    PAYLOAD : udp_message_command_get_server_info_payload_t

class udp_message_command_get_server_info_reply_t(BaseModel):
    MESSAGE_TYPE : message_type_t
    PAYLOAD : udp_message_command_get_server_info_reply_payload_t


#todo : write all message type...