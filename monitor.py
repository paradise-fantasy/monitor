#!/usr/bin/python

import subprocess
import sys
import time
import pathos.multiprocessing as mp

from os import system
from host import host
from functools import partial


class monitor:
     
    def __init__(self,hostfile,oidfile):
        self.hosts = []
        self.oids = []
        self.recentData = {}
        self.setHosts(hostfile)
        self.setOids(oidfile)
        self.pool = mp.ProcessingPool(len(self.hosts))

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
                h = host(data[0],data[1])
                self.hosts.append(h)
            f.close()
        

    def setOids(self, filename):
        if (self.fileCheck(filename)):
            f = open(filename, "r")
            for line in f.readlines():
                data = line.rstrip('\n')
                self.oids.append(data)
                for h in self.hosts:
                    h.appendOid(data)
            f.close()
            
    def fetchData(self,h):
        return h.getData()

    def update(self):
        func = partial(self.fetchData)
        results = self.pool.map(func, tuple(self.hosts))
        for resultDictionary in results:
            self.recentData[resultDictionary['sysName.0'][0]]=resultDictionary

    def sendToLog(self):
        for key in self.recentData.keys():
            print key +" :: " + str(self.recentData[key])



if __name__ == "__main__":
    m = monitor(sys.argv[1],sys.argv[2])
    print("starting monitor")
    m.update()
    m.sendToLog()

    

