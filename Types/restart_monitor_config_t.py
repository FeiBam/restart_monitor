from dataclasses import dataclass
from Types.server_config_t import server_config_t
from utils.JsonSerializable import JsonSerializable



@dataclass
class restart_monitor_config_t(JsonSerializable):
    Type: str
    ServerConfig : server_config_t