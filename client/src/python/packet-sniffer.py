from scapy.all import *
import requests
import sys
import json

connectionID = -1
serverAddr = "49.247.197.181"
serverPort = "8000"

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

def sendData(packet):
    packet_dict = packetFormatter(packet)
    r = {}

    if ("IP" in packet_dict):
        dst_ip = packet_dict["IP"]["dst"]
        if (dst_ip != serverAddr):
            destination = "http://" + serverAddr + ":" + serverPort + "/users/" + str(connectionID) + "/packet"
            r = requests.post(destination, data={"data": json.dumps(packet_dict)}).text

    # if not r:
    #     print("ERROR: Server doesn't answer")
    # else:
    #     if r['code'] != 1:
    #         print("ERROR: " + r['code'])

if __name__ == "__main__":
    if sys.argv[1]:
        connectionID = sys.argv[1]

    if (connectionID == -1):
        print(-1)
        print("ERROR: Undefined Connection ID")
    else:
        getNetActivity()
