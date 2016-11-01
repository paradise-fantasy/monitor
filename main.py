#!/usr/bin/python

import sys
import paho.mqtt.publish as publish
from json import JSONEncoder
from monitor import monitor


def readData():
    f = open("valueStore")
    if f.read()=='':
        return None
    data = json.load(f)
    return data


def writeData(data):
    f = open("valueStore","w")
    json.dumps(data,f)


def reorder(data):
    tempStore = {}
    for subset in data:
        tempStore[subset['host']]=subset
    return tempStore


def sendToLog(data):
    publish.single("paradise/test/monitor",JSONEncoder().encode(data), port=8883, tls={'ca_certs':"ca.crt",'tls_version':2}, hostname="nyx.bjornhaug.net")
    publish.single("paradise/testlog/monitor","Alive=True", port=8883, tls={'ca_certs':"ca.crt",'tls_version':2}, hostname="nyx.bjornhaug.net")

if __name__ == "__main__":
    m = monitor(sys.argv[1],sys.argv[2])
    rawData = m.update()
    processedData = reorder(rawData)
    sendToLog(processedData)
