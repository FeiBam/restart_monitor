from dataclasses import dataclass

@dataclass
class discover_service_config:
    discoverDleay : int
    senderPort : int
    listennerPort : int