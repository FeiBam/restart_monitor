import socket
import Core.Server as Server
import Core.Client as Client
from Service.UDPService import UDPService
import json


def main():
    monitorInstance = None
    with open("settings.json") as configFils:
        config = json.load(configFils)
    
    if config.Type == "Client":
        monitorInstance = getClientInstance()

    if config.Type == "Server":
        monitorInstance = getServerInstance()
    
    monitorInstance.run()
    
def getClientInstance(config = None):
    if not config:
        config = {
            "listennerPort":36618,
            "senderPort":36681
        }
    instacne = Client.RestartMonitorClient(config, UDPService.UDPService)
    
def getServerInstance(config = None):
    if not config:
        config = {
            "listennerPort":36618,
            "senderPort":36681,
            "discoverDleay" : 3600
        }
    instance = Server.RestartMonitorServer(config, UDPService.UDPService)
    
