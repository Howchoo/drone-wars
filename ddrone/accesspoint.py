class AccessPoint:
    
    def __init__(self, s, m=None, c=None):
        
        self.ssid = s
        self.mac = m
        self.channel = c
        self.key = None
        self.dumpfilename = s
        
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.ssid == other.ssid
        else:
            return False
        
    def __str__(self):
        
        return '<SSID: ' + str(self.ssid) + ', MAC: ' + str(self.mac) + ', CHANNEL: ' + str(self.channel) + '>'
        