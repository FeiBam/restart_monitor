import argparse
import socket
import json
from Service.UDPService import UDPService
from Core.Server import RestartMonitorServer
from Core.Client import RestartMonitorClient
from utils.Logger import ClassNameLogger, get_class_name_logger

from Types.server_config_t import server_config_t
from Types.client_config_t import client_config_t
from Types.udp_message_t import udp_message_t, message_type_t
from Types.command_t import *        
from Types.restart_monitoy_type_t import restart_monitoy_type_t


class RestartMonitorCLI():
    def __init__(self):
        self.logger = get_class_name_logger("RestartMonitor", "CLI")
        self.udp_server_instance = UDPService.buildServer(socket.AF_INET, "127.0.0.1", 36615)
        self.udp_server_instance.register_handler(self.handler_udp_message)
        self.udp_server_instance.listener()
        self.local_service_type = None
        self.client = None  # Assuming this will be initialized properly
        message = udp_message_t(
            MESSAGE_TYPE = message_type_t.COMMAND.value,
            PAYLOAD = command_service_type_t(
                COMMAND=command_t.SERVICE_TYPE.value
            )
        )
        self.udp_server_instance.send_strings(("127.0.0.1", 36616),message.model_dump_json())
        

    def handler_udp_message(self, size, data: bytes, addr):
        print(data)
        data = data.decode("utf-8")
        print(data)
        message = udp_message_t.model_validate_json(data)
        print(message)
        if message.MESSAGE_TYPE.value == message_type_t.MESSAGE.value:
            if message.PAYLOAD.COMMAND.value == command_t.SERVICE_TYPE.value:
                    if message.PAYLOAD.DATA.value == restart_monitoy_type_t.CLIENT.value:
                        self.local_service_type = restart_monitoy_type_t.CLIENT.value
                    elif message.PAYLOAD.DATA.value == restart_monitoy_type_t.SERVER.value:
                        self.local_service_type = restart_monitoy_type_t.SERVER.value
        
    def run(self):
        self.udp_server_instance.start()
        while True:
            try:
                command = input("client> ").strip().lower()
                if command == "show devices":
                    if self.local_service_type != restart_monitoy_type_t.SERVER.value:
                        print("Local Service Is Client Mode..")
                        continue

                elif command == "stop":
                    self.client.stop()
                    return
                
                elif command == "restart":
                    if self.local_service_type != restart_monitoy_type_t.SERVER.value:
                        print("Local Service Is Client Mode..")
                        continue
                    self.client.restart()

                elif command == "info":
                    if self.local_service_type == restart_monitoy_type_t.SERVER.value:
                        pass

                    elif self.local_service_type == restart_monitoy_type_t.CLIENT.value:
                        pass

                    message = udp_message_t(
                        MESSAGE_TYPE=message_type_t.COMMAND,
                        PAYLOAD=command_get_server_info_t(
                            COMMAND=command_t.INFO,
                        )
                    )

                    self.udp_server_instance.send_strings(("127.0.0.1", 36616),message.model_dump_json())

                elif command == "type":
                    print(self.local_service_type)

                elif command == "help":
                    print("Available commands: show devices, restart, info, exit")

                elif command == "exit":
                    print("Bye~ Have Nice Day.")
                    self.udp_server_instance.stop()
                    return

                else:
                    print(f"Unknown command: {command}")

            except KeyboardInterrupt:
                self.logger.info("KeyboardInterrupt detected. Exiting...")
                self.udp_server_instance.stop()
                return
            except EOFError:
                self.logger.info("KeyboardInterrupt detected. Exiting...")
                self.udp_server_instance.stop()
                return


def main():
    cli = RestartMonitorCLI()
    cli.run()


if __name__ == "__main__":
    main()