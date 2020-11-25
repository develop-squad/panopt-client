import psutil
import requests
import sys
import json

connectionID = -1
serverAddr = "49.247.197.181"
serverPort = "8000"

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

def sendData(processList):
    destination = "http://" + serverAddr + ":" + serverPort + "/users/" + str(connectionID) + "/process"
    r = requests.post(destination, data={"data": json.dumps(processList)}).text
    
    if not r:
        print("ERROR: Server doesn't answer")
    else:
        if r['code'] != 1:
            print("ERROR: " + r['code'])


if __name__ == "__main__":
    if sys.argv[1]:
        connectionID = sys.argv[1]

    if (connectionID == -1):
        print(-1)
        print("ERROR: Undefined Connection ID")
    else:
        processList = getNetActivity()
        print(processList)
        sendData(processList)
