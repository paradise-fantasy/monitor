#!/usr/bin/python

import subprocess


class host:

    def __init__(self,ip,community):
        self.data = {}
        self.oids = []
        self.ip = ip
        self.community = "-c "+community
        self.version = "-v 2c"

    def getName(self):
        return self.name

    def getIp(self):
        return self.ip

    def getOids(self):
        global oids
        return self.oids


    def getData(self):
        for oid in self.getOids():
            p = subprocess.Popen(["snmpwalk %s %s %s %s" %(self.community,self.version,self.ip,oid)],stdout=subprocess.PIPE, shell=True)
            out, err = p.communicate()
            out.split('\n')
            out = out[:-1]
            multiValueStore = []
            for line in out.split('\n'):
                multiValueStore.append(line.split(":")[-1].rstrip('\r\n').lstrip())
            self.data[oid]=tuple(multiValueStore)   
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

