import argparse
import socket
import json
from Service.UDPService import UDPService
from Core.Server import RestartMonitorServer
from Core.Client import RestartMonitorClient
from utils.Logger import ClassNameLogger, get_class_name_logger
 
from Types.server_config_t import server_config_t
from Types.client_config_t import client_config_t
from Types.udp_message_t import *
from Types.command_t import *        
from Types.restart_monitoy_type_t import restart_monitoy_type_t
from time import sleep

exitSingal = False

def load_config(config_path, logger):
    try:
        with open(config_path) as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        logger.error("Setting File Not Found!")
        return None
    except json.JSONDecodeError:
        logger.error("Invalid JSON in the settings file!")
        return None

def build_client_command_service(client : RestartMonitorClient):
    udp_command_server_instance = UDPService.buildServer(socket.AF_INET, "0.0.0.0", 36616)
    udp_command_server_instance.listener()

    def handler_udp_message(data_length: int, data: bytes, address: tuple):
        data = data.decode("utf-8")
        json_data = json.loads(data)
        message = udp_message_t(**json_data)
        if message.MESSAGE_TYPE == message_type_t.COMMAND.value:
            handler_command(message.PAYLOAD.COMMAND.value)

    def handler_command(command):
        if command == command_t.SERVICE_TYPE.value:
            client.logger.info("Command Request Service Type.")
            data = udp_message_t(
                MESSAGE_TYPE = message_type_t.MESSAGE,
                PAYLOAD = command_service_type_reply_t(
                    COMMAND = command_t.SERVICE_TYPE,
                    DATA = restart_monitoy_type_t.CLIENT
                ).model_dump()
            )
            udp_command_server_instance.send_strings(("127.0.0.1",36615),data.model_dump_json())
        if command == command_t.EXIT.value:
            client.stop()
    
    udp_command_server_instance.register_handler(handler_udp_message)
    udp_command_server_instance.start()

def build_server_command_service(server : RestartMonitorServer):
    udp_command_server_instance = UDPService.buildServer(socket.AF_INET, "0.0.0.0", 36616)
    udp_command_server_instance.listener()
    
    def handler_udp_message(data_length: int, data: bytes, address: tuple):
        data = data.decode("utf-8")
        json_data = json.loads(data)
        message = udp_message_t(**json_data)
        if message.MESSAGE_TYPE.value == message_type_t.COMMAND.value:
            handler_command(message.PAYLOAD.COMMAND.value) 

    def handler_command(command):
        if command == command_t.SERVICE_TYPE.value:
            server.logger.info("Command : Request Service Type.")
            data = udp_message_t(
                MESSAGE_TYPE = message_type_t.MESSAGE,
                PAYLOAD = command_service_type_reply_t(
                    COMMAND = command_t.SERVICE_TYPE,
                    DATA  =  restart_monitoy_type_t.CLIENT
                )
            )
            print(data.model_dump_json())
            udp_command_server_instance.send_strings(("127.0.0.1",36615),data.model_dump_json())

        if command == command_t.RESTART.value:
            server.logger.info("Command : fouce restart...")
            server.restart()

        if command == command_t.INFO.value:
            server.logger.info("Command :  GET Server Info.")
            data =  udp_message_t(
                MESSAGE_TYPE = message_type_t.MESSAGE,
                PAYLOAD = comand_get_server_info_reply_t(
                    COMMAND = command_t.INFO,
                    DATA = server.restart_info
                ).model_dump()
            )
            udp_command_server_instance.send_strings(("127.0.0.1",36615),data.model_dump_json())

        if command == command_t.EXIT.value:
            server.stop()

        if command == command_t.SHOW_DEVICE.value:
            data = udp_message_t(
                MESSAGE_TYPE = message_type_t.MESSAGE,
                PAYLOAD = command_get_devices_reply_t(
                    DATA= [device.to_dict() for device in server.Devices]
                ).model_dump()
            )
            udp_command_server_instance.send_strings(("127.0.0.1",36615),data.model_dump_json())

    udp_command_server_instance.register_handler(handler_udp_message)
    udp_command_server_instance.start()

def parse_arguments():
    parser = argparse.ArgumentParser(description="Restart Monitor")
    parser.add_argument('--config', required=True, help='Server address')
    return parser.parse_args()

def main():
    logger = get_class_name_logger("Main", "MAIN FUNC")
    args = parse_arguments()
    config_path = args.config
    config = load_config(config_path, logger)

    if config["Type"] == "Server":
        server_config = server_config_t.model_validate(config['ServerConfig'])
        udp_server_instance = UDPService.buildServer(socket.AF_INET, "0.0.0.0", server_config.ListenerPort)
        udp_server_instance.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        server = RestartMonitorServer(server_config, udp_server_instance)
        server.start()
        build_server_command_service(server)

    elif config["Type"] == "Client":
        client_config = client_config_t.model_validate(config["ClientConfig"])
        udp_server_instance = UDPService.buildServer(socket.AF_INET, "0.0.0.0", client_config.ListenerPort)
        client = RestartMonitorClient(client_config, udp_server_instance)
        client.start()
        build_client_command_service(client)

    else:
        logger.error("Invalid config type specified.")
        return False
    
    while True:
        if exitSingal:
            return
        sleep(1)

def m():
    data = udp_message_command_get_service_type_reply_t(
        MESSAGE_TYPE = message_type_t.MESSAGE,
        PAYLOAD = udp_message_command_get_service_type_reply_payload_t(
            COMMAND = command_t.SERVICE_TYPE,
            DATA = restart_monitoy_type_t.SERVER
        )
    )
    print(data.model_dump_json())
    
#todo  change all udp_message_t to corresponding message type
if __name__ ==  "__main__":
    m()


    
