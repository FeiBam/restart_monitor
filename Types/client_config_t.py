

from dataclasses import dataclass
from pydantic import BaseModel

@dataclass
class client_config_t(BaseModel):
    SenderPort : int
    ListenerPort : int