#!/usr/bin/python

from host import host
import subprocess
import sys
from os import system

class monitor:
    hosts = []
    def __init__(self,hostfile,oidfile):
        self.setHosts(hostfile)
        self.setOids(oidfile)
        self.main()

    def fileCheck(self,filename):
        try:
            f = open(filename)
            return True
        except IOError as e:
            print ("%s does not exist!" % e)
            return False

    def setHosts(self, filename):
        if (self.fileCheck(filename)):
            f = open(filename, "r")
            for line in f.readlines():
                data = line.strip().split(";")
                h = host(data[0],data[1],data[2],"2c")
                self.hosts.append(h)
            f.close()
        

    def setOids(self, filename):
        if (self.fileCheck(filename)):
            f = open(filename, "r")
            for line in f.readlines():
                data = line.rstrip('\n')
                for h in self.hosts:
                    h.appendOid(data)
            

    def getData(self):
        data = {}
        for h in self.hosts:
            data[h.getName()] = h.getData()
       

    def main(self):
        self.getData()

m = monitor(sys.argv[1],sys.argv[2])
    

