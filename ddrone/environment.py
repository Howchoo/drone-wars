from accesspoint import AccessPoint
import commands

class Environment:
    
    def __init__(self, d=None, s=None):
        
        self.device = d
        self.ssid = s
        self.accesspoints = None
        self.initialized = False
        
        if (d and s):
            self.__initialize(d, s)
        
    def __initialize(self, d, s):
        
        self.device = d
        self.ssid = s
        self.accesspoints = self.__getaccesspoints(d, s)
        self.initialized = True

    def __getaccesspoints(self, device, ssid):

        out = commands.searchssid(device, ssid)
        ssids = filter(lambda item: len(item) > 0, map(lambda line: (line.replace('SSID:','')).strip(), out.split('\n')))
        accesspoints = map(lambda ssid: AccessPoint(ssid), ssids)

        return accesspoints