

from dataclasses import dataclass
from Types.discover_service_config_t import discover_service_config_t
from Types.restart_time_setting_t import restart_time_setting_t
from pydantic import BaseModel


@dataclass
class server_config_t(BaseModel):
    DiscoverConfig : discover_service_config_t
    RestartAT : restart_time_setting_t
    RestartDelay: int
    DeviceTimeOut : int
    DeviceUpdateDelay : int
    SenderPort : int
    ListenerPort : int
