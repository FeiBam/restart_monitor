from dataclasses import dataclass
from pydantic import BaseModel


@dataclass
class discover_service_config_t(BaseModel):
    DiscoverDelay : int
    SenderPort : int
