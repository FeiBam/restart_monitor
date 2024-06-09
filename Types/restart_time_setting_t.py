

from dataclasses import dataclass
from utils.JsonSerializable import JsonSerializable

@dataclass
class restart_time_setting_t(JsonSerializable):
    month: int
    day : int
    weekly : int
    hour : int
    minute : int
    second : int
