import psutil
import requests
import sys
import json

serverAddr = "49.247.197.181"
serverPort = "8000"

def errorPrint(msg):
    print("ERROR: " + msg)

def getNetActivity():
    processList = {}
    for conn in psutil.net_connections():
        newInfo = {}
        if conn.status == 'NONE':
            continue
        if not conn.raddr:
            continue
        if conn.raddr[0] == serverAddr:
            continue
        
        newInfo["name"] = psutil.Process(conn.pid).name()
        newInfo["status"] = conn.status
        newInfo["local_ip"] = conn.laddr[0]
        newInfo["local_port"] = conn.laddr[1]
        newInfo["remote_ip"] = conn.raddr[0] if conn.raddr else ''
        newInfo["remote_port"] = conn.raddr[1] if conn.raddr else ''

        processList[conn.pid] = newInfo

    return processList

if __name__ == "__main__":
    processList = getNetActivity()
    print(json.dumps(processList))
