

from dataclasses import dataclass
from Types.discover_service_config_t import discover_service_config_t
from Types.restart_time_setting_t import restart_time_setting_t
from utils.JsonSerializable import JsonSerializable


@dataclass
class server_config_t(JsonSerializable):
    DiscoverConfig : discover_service_config_t
    RestartAT : restart_time_setting_t
    RestartDelay: int
    DeviceTimeOut : int
    DeviceUpdateDelay : int
    SenderPort : int
    ListenerPort : int
