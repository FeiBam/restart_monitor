from abc import ABC, abstractmethod


class udp_callback_interface_t(ABC):
    
    @abstractmethod
    def handle_message(self, data_length: int, data: bytes, address: tuple):
        pass