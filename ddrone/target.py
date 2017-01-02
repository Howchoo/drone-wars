import accesspoint

class Target:
    
    def __init__(self, m, ap):
        
        self.mac = m
        self.accesspoint = ap
        
    def __str__(self):
        
        return '<MAC: ' + str(self.mac) + ', ACCESS POINT: ' + str(self.accesspoint) + '>'
        