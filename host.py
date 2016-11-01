#!/usr/bin/python

import subprocess
import re

class host:

    def __init__(self,ip,community):
        self.data = {}
        self.oids = []
        self.ip = ip
        self.community = "-c "+community
        self.version = "-v 2c"
        self.setName()

    def getName(self):
        return self.name

    def getIp(self):
        return self.ip

    def getOids(self):
        global oids
        return self.oids

    def setName(self):
        p = subprocess.Popen(["snmpget %s %s %s %s" %(self.community,self.version,self.ip,"sysName.0")],stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        try:
            self.name = out.split()[-1]
        except IndexError:
            self.name = "__destroy__"


    def checkIfUpTime(self,data):
        if "sysUpTime" in data:
            return True
        return False

    def getData(self):
        for oid in self.getOids():
            p = subprocess.Popen(["snmpwalk %s %s %s %s" %(self.community,self.version,self.ip,oid)],stdout=subprocess.PIPE, shell=True)
            out, err = p.communicate()
            out.split('\n')
            out = out[:-1]
            multiValueStore = []
            for line in out.split('\n'):
                if (self.checkIfUpTime(line)):
                    time = [int(s) for s in re.findall(r'\b\d+\b',line.split(")")[-1].lstrip())]
                    text = ""
                    index = 0

                    if (len(time)>4):
                        days = time[index]
                        textDays = " dager " if days > 1 else " dag "
                        text = str(days)+textDays
                        index+=1
                    if (len(time)==4):
                        index = 0
                    if (len(time)>3):
                        hours = time[index]
                        textHours = " timer " if hours > 1 else " time "
                        text += str(hours)+textHours
                        index+=1
                    if (len(time)>2):
                        minutes = time[index]
                        textMinutes = " min " if minutes > 1 else " min "
                        text += str(minutes)+textMinutes
                        index+=1
                    if (len(time)>1):
                        seconds = time[index]
                        textSeconds = " sek" if seconds > 1 else " sek"
                        text += str(seconds)+textSeconds
                    
                    multiValueStore.append(text)
                else:
                    multiValueStore.append(line.split(":")[-1].rstrip('\r\n').lstrip())
            self.data[oid.split('.')[0]]=tuple(multiValueStore)
        self.data["host"]=self.name
        return self.data
    

    def appendOid(self,oid):
        self.oids.append(oid)

    
    def removeOid(self,oid):
        if (self.oids.remove(oid)):
            return True
        return False


#h = host("sahara30.item.ntnu.no","sahara30","ttm4128","2c")
#h.appendOid("SNMPv2-MIB::sysName.0")
#print(h.getData())

