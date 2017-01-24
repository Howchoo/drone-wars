import accesspoint

class Target:
    
    def __init__(self, m, ap):
        
        self.mac = m
        self.accesspoint = ap
        
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.mac == other.mac
        else:
            return False
        
    def __str__(self):
        
        return '<MAC: ' + str(self.mac) + ', ACCESS POINT: ' + str(self.accesspoint) + '>'
        