#!/usr/bin/python

import sys
import paho.mqtt.publish as publish
from json import JSONEncoder
import json
from monitor import monitor
import time

def readData():
    try:
        f = open("valueStore")
    except IOError:
        return None
    data = json.load(f)
    return data


def writeData(host,topic,newData):
    data = readData()
    if data==None:
        data = {}
    f = open("valueStore","w")
    if host in data.keys():
        data[host][topic]=newData
    else:
        data[host]={}
        data[host][topic]=newData
    data[host]["Time"]=time.time()
    f.write(json.dumps(data,f))
    f.close()


def reorder(data):
    tempStore = {}
    for subset in data:
        subset["Memory"]=calculateMemory(subset['memAvailReal'][0],subset['memTotalReal'][0])
        del subset['memAvailReal']
        del subset['memTotalReal']
        subset["Bandwidth"]=calculateBandwidth(subset['host'],subset['ifInOctets'][0])
        del subset['ifInOctets']
        subset["Uptime"]=subset["sysUpTimeInstance"]
        del subset["sysUpTimeInstance"]
        subset["Host"]=[subset["host"]]
        del subset["host"]
        subset["Load"]=[subset["laLoad"]]
        del subset['laLoad']
        tempStore[subset['Host'][0]]=subset
    return tempStore

def calculateMemory(avail,total):
    return [str("%.2f") % (float(avail.split()[0])/float(total.split()[0])*100)+" %"]


def calculateBandwidth(host,incomming):
    oldData = readData()
    if oldData==None or (host not in oldData.keys() and isinstance(oldData, dict)):
        writeData(host,"Bandwidth",incomming)
        return "x bytes/sec"
    sec = time.time()-oldData[host]["Time"]
    bandwidth=["%.2f" %(float((float(incomming)-float(oldData[host]["Bandwidth"]))/(sec*1024*1024/8))) +" Mbit/sec"]
    writeData(host,"Bandwidth",incomming) 
    return bandwidth
    
def addDeadHosts(data):
    oldData = readData()
    if oldData == None:
        return data

    for host in oldData.keys():
        if host not in data.keys():
            data[host]={}
            data[host]["Host"]=[host]
            data[host]["Uptime"]=["DOWN"]
            data[host]["Bandwidth"]=["0.00 Mbit/sec"]
            data[host]["Memory"]=["110 %"]
            data[host]["Load"]=["0.00", "0.00", "0.00"]
    return data

    
def sendToLog(data):
    publish.single("paradise/test/monitor",JSONEncoder().encode(data), port=8883, tls={'ca_certs':"ca.crt",'tls_version':2}, hostname="nyx.bjornhaug.net")
    publish.single("paradise/testlog/monitor","Alive=True", port=8883, tls={'ca_certs':"ca.crt",'tls_version':2}, hostname="nyx.bjornhaug.net")

if __name__ == "__main__":
    m = monitor("hosts.txt","oids.txt")
    rawData = m.update()
    processedData = reorder(rawData)
    processedData = addDeadHosts(processedData)
    sendToLog(processedData)
