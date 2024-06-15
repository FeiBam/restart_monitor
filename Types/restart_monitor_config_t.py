from dataclasses import dataclass
from Types.server_config_t import server_config_t
from pydantic import BaseModel
from Types.restart_monitoy_type_t import restart_monitoy_type_t


@dataclass
class restart_monitor_config_t(BaseModel):
    Type: restart_monitoy_type_t
    ServerConfig : server_config_t