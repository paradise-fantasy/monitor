#!/usr/bin/python

import subprocess


class host:
    data = {}
    oids = []
    ip = "127.0.0.1"
    name = "localhost"
    community = "default"
    version = "2c"

    def __init__(self,ip,name,community,version):
            self.ip = ip
            self.name = name
            self.community = "-c "+community
            self.version = "-v "+version

    def getName(self):
        return self.name

    def getIp(self):
        return self.ip

    def getOids(self):
        return self.oids


    def getData(self):
        for oid in self.getOids():
            p = subprocess.Popen(["snmpget %s %s %s %s" %(self.community,self.version,self.ip,oid)],stdout=subprocess.PIPE, shell=True)
            out, err = p.communicate()
            self.data[oid]=out.split()[-1]
        return self.data

    def appendOid(self,oid):
        if (self.oids.append(oid)):
            return True
        return False
        
    
    def removeOid(self,oid):
        if (self.oids.remove(oid)):
            return True
        return False




