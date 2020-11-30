import sys
import psutil
import os
import signal
import csv
import json

def errorPrint(msg):
    print("ERROR: " + msg)

def blockProcess(pid):
    path = ""
    try:
        path = psutil.Process(pid).exe()
    except:
        errorPrint("PID error")
        exit()

    try:
        os.popen('netsh advfirewall firewall add rule name="panopt-INBOUND-'+path+'" dir=in action=block program= "'+path+'" enable=yes profile=any')
        os.popen('netsh advfirewall firewall add rule name="panopt-OUTBOUND-'+path+'" dir=out action=block program= "'+path+'" enable=yes profile=any')
    except:
        print(-1)
        errorPrint("Firewall error")
        exit()

    try:
        with open('ProcessBlockList.txt', 'at', encoding='utf-8') as data_file:
            data_file.write(path+'\n')
    except:
        print(-1)
        errorPrint("File I/O error")
    
    print(1)


def blockCountry(countryCode):
    rangeList = []
    try:
        with open('country_data.csv', 'r', encoding='utf-8') as csv_file:
            csv_data = csv.reader(csv_file)

            for data in csv_data:
                if csv_data[1] == countryCode:
                    rangeList.append(data[2] + data[4])
    except:
        print(-1)
        errorPrint("Data file open error")
        exit()
        
    i = 0
    for ipRange in rangeList:
        try:
            os.popen('netsh advfirewall firewall add rule name="panopt-INBOUND-'+countryCode+'-'+str(i)+'" dir=in action=block RemoteIP="'+ipRange+'" enable=yes profile=any')
            os.popen('netsh advfirewall firewall add rule name="panopt-OUTBOUND-'+countryCode+'-'+str(i)+'" dir=out action=block RemoteIP="'+ipRange+'" enable=yes profile=any')
        except:
            print(-1)
            errorPrint("Firewall error")
            exit()
        i += 1

    try:
        with open('CountryBlockList.txt', 'at', encoding='utf-8') as data_file:
            data_file.write(countryCode+'-'+str(i)+'\n')
    except:
        print(-1)
        errorPrint("File I/O error")

    print(1)

def releaseProcess(path):
    try:
        os.popen('netsh advfirewall firewall delete rule name="panopt-INBOUND-'+path+'"')
        os.popen('netsh advfirewall firewall delete rule name="panopt-OUTBOUND-'+path+'"')
    except:
        print(-1)
        errorPrint("Firewall error")
        exit()

    print(1)

def releaseCountry(value):
    countryCode = value.split('-')[0]
    index = value.split('-')[1]
    try:
        for i in range(0, index):
            os.popen('netsh advfirewall firewall delete rule name="panopt-INBOUND-'+countryCode+'-'+str(i)+'"')
            os.popen('netsh advfirewall firewall delete rule name="panopt-OUTBOUND-'+countryCode+'-'+str(i)+'"')
    except:
        print(-1)
        errorPrint("Firewall error")
        exit()

    print(1)

def killProcess(pid):
    try:
        psutil.Process(pid).kill()
    except:
        print(-1)
        errorPrint("Invailed process info")
        return

def blockList():
    try:
        with open('ProcessBlockList.txt', 'r', encoding='utf-8') as file_data:
            processList = file_data.readlines()
    except:
        processList = []

    try:
        with open('CountryBlockList.txt', 'r', encoding='utf-8') as file_data:
            countryList = file_data.readlines()
    except:
        countryList = []
    
    print(processList)
    print(countryList)

if __name__ == "__main__":
    mode = -1
    value = -1
    
    try:
        if sys.argv[1]:
            mode = sys.argv[1]
        else:
            print(-1)
            errorPrint("Invailed mode selection")
            exit()
        
        if sys.argv[2]:
            value = sys.argv[2]
        else:
            print(-1)
            errorPrint("Invailed value selection")
            exit()
    except:
        print(-1)
        errorPrint("Invailed argument value")
        exit()
    
    if mode == 1:
        blockProcess(value)
    elif mode == 2:
        releaseProcess(value)
    elif mode == 3:
        blockCountry(value)
    elif mode == 4:
        releaseCountry(value)
    elif mode == 5:
        blockList()
    elif mode == 6:
        killProcess(value)
    else:
        print(-1)
        errorPrint("Wrong mode selection")
