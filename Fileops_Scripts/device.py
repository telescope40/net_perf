#Louis DeVictoria
#Class to parse Librenms Data from API Calls


#device_id
#hostname
#sysName
#ip
#hardware
#os
#sysDescr
#serial

class Device():
    '''Class to pull in values from librenms'''
    def __init__(self, hostname,ip,os,hardware,serial,sysDescr ):
        self.hostname = hostname
        self.ip = ip
        self.os = os
        self.hardware = hardware
        self.serial = serial
        self.sysDescr = sysDescr

    def getdesc(self):
        '''return a formatted description'''
        desc = f'Hostname: {self.hostname}\n'\
               f'IP: {self.ip}\n'\
               f'Platform: {self.os}\n'\
               f'Hardware: {self.hardware}\n'\
               f'Serial: {self.serial}\n'\
               f'SysDescr: {self.sysDescr}\n'
        return desc

    def createdict(self):
        data = {}
        data[self.hostname] = [self.ip,self.os,self.hardware,self.serial,self.sysDescr]
        return data