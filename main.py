import socket
from Service.UDPService import UDPService
from Types.server_config_t import server_config_t
from Core.Server import RestartMonitorServer
import json

        

def main():

    def discoverHandler(size, data, addr):
        print(size, data, addr)


    configFile = open("settings.json")
    config = json.load(configFile)
    server_config = server_config_t.from_dict(config['ServerConfig'])

    x = 0
    monitorInstance = None
    udpClientInstance  = UDPService.buildClient(socket.AF_INET, 1)
    udpServerInstance = UDPService.buildServer(socket.AF_INET, "0.0.0.0" , 36618)
    udpServerInstance.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server = RestartMonitorServer(server_config, udpServerInstance)

    server.start()


    while True:
        try:
            command = input()
            command.lower()
            if command == "show devices":
                server.logger.info(server.Devices)
            if command == "exit":
                server.stop()
                return
            if command == "restart":
                server.restart()
            if command == "info":
                print(server.restart_info)
        except KeyboardInterrupt:
            if x == 2:
                server.stop()
                return
            x+=1
            continue
    
            


if __name__ ==  "__main__":
    main()



    
