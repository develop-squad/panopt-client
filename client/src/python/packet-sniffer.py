from scapy.all import *
import psutil
import requests
import sys
import json

connectionID = -1
serverAddr = "49.247.197.181"
serverPort = "8000"
sames = 0
packets = 0

def errorPrint(msg):
    print("ERROR: " + msg)

def getNetActivity():
    sniff(count=0, prn=sendData)
    
def packetFormatter(packet):
    packet_dict = {}
    for line in packet.show2(dump=True).split('\n'):
        if '###' in line:
            layer = line.strip('#[] ')
            packet_dict[layer] = {}
        elif '=' in line:
            key, val = line.split('=', 1)
            packet_dict[layer][key.strip()] = val.strip()

    return packet_dict

def getProcessActivity():
    processList = {}
    for conn in psutil.net_connections():
        newInfo = {}
        if conn.status == 'NONE':
            continue
        if not conn.raddr:
            continue
        if conn.raddr[0] == serverAddr:
            continue
        
        try:
            newInfo["name"] = psutil.Process(conn.pid).name()
        except:
            return -1

        newInfo["status"] = conn.status
        newInfo["local_ip"] = conn.laddr[0]
        newInfo["local_port"] = conn.laddr[1]
        newInfo["remote_ip"] = conn.raddr[0] if conn.raddr else ''
        newInfo["remote_port"] = conn.raddr[1] if conn.raddr else ''

        processList[conn.pid] = newInfo

    return processList

def sendData(packet):
    global sames

    packet_dict = packetFormatter(packet)
    process_dict = getProcessActivity()
    if (process_dict == -1):
        return
    
    if ("IP" in packet_dict):
        dst_ip = packet_dict["IP"]["dst"]
        src_ip = packet_dict["IP"]["src"]

        pid = -1
        exist = False
        for process in process_dict:
            if ((dst_ip == process_dict[process]['remote_ip'] and src_ip == process_dict[process]['local_ip']) or (src_ip == process_dict[process]['remote_ip'] and dst_ip == process_dict[process]['local_ip'])):
                pid = process
                exist = True
                break
        if (dst_ip != serverAddr and exist):
            sames += 1
            destination = "http://" + serverAddr + ":" + serverPort + "/users/" + str(connectionID) + "/packet"

            response = {}
            response["packet"] = packet_dict
            response["process"] = process_dict[pid]

            try:
                r = requests.post(destination, data={"data": json.dumps(response)}).text
            except:
                print(-1)
                errorPrint("Server connection error")
                exit()

            print(process_dict[pid]['name'])
            
            if not r:
                print(-1)
                errorPrint("Server doesn't answer")
            else:
                r = json.loads(r)
                if r['code']:
                    if r['code'] != 1:
                        print(-1)
                        errorPrint("Server error: " + str(r['code']))
                else:
                    print(-1)
                    errorPrint("Server error: Unexpected response")

if __name__ == "__main__":
    try:
        if sys.argv[1]:
            connectionID = sys.argv[1]
    except:
        print(-1)
        errorPrint("Invailed argument value")
        exit()
    
    if (connectionID == -1):
        print(-1)
        errorPrint("Undefined Connection ID")
    else:
        getNetActivity()
