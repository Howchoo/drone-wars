from accesspoint import AccessPoint
import commands
import re

class Environment:
    
    def __init__(self, d=None, s=None, v=False):
        
        self.device = d
        self.ssid = s
        self.accesspoints = None
        self.initialized = False
        self.verbose = v
        
        if (d and s):
            self.initialize(d, s)
        
    def initialize(self, d, s):
        
        self.device = d
        self.ssid = s
        self.accesspoints = self.__getaccesspoints(d, s)
        self.initialized = True
        
        if self.verbose:
            print "Environment initialized!"
            
            
    def crackdrone(self, index):
        
        if index < len(self.accesspoints):
            print 'Cracking ' + str(self.accesspoints[index])
            self.__startmonitormode(index)
        else:
            print 'Out of bounds! Only ' + len(self.accesspoints) + ' drones found.'
            

    def __getaccesspoints(self, device, ssid):

        out = commands.searchssid(device, ssid, after=2)
        
        def createaccesspoint(ssidinfo):
            ssid = ''.join(filter(lambda line: 'SSID:' in line, ssidinfo.split('\n'))).replace('SSID:','').strip()
            channel = ''.join(filter(lambda line: 'DS Parameter set: channel' in line, ssidinfo.split('\n'))).replace('DS Parameter set: channel','').strip()
            return AccessPoint(s=ssid, c=channel)
        
        accesspoints = map(lambda ssidinfo: createaccesspoint(ssidinfo), out.split('--'))
        
        if self.verbose:
            print "FOUND: " + str(map(lambda accesspoint: str(accesspoint), accesspoints))

        return accesspoints
    
    
    def __startmonitormode(self, index):
        
        accesspoint = self.accesspoints[index]
        commands.airmoncheckkill()
        commands.disabledevice(self.device)
        out = commands.startmonitormode(self.device, accesspoint.channel)

        return re.match(r'(.*)](.*)\)', ''.join(filter(lambda line: 'monitor mode vif enabled' in line, out.split('\n')))).groups('0')[1]
        
        
    