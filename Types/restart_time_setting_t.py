

from dataclasses import dataclass
from pydantic import BaseModel

@dataclass
class restart_time_setting_t(BaseModel):
    month: int
    day : int
    weekly : int
    hour : int
    minute : int
    second : int
