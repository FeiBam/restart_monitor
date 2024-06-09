from dataclasses import dataclass
from utils.JsonSerializable import JsonSerializable



@dataclass
class discover_service_config_t(JsonSerializable):
    DiscoverDelay : int
    SenderPort : int
