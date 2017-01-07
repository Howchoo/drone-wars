import sys
import time
import commands
from environment import Environment


"""
ddrone - drone cracking made easy

Written for OpenWERX Drone Vulnerabilities Challenge

Author: Jeremy Smith
License: GPL
"""


def main():
    
    env = None

    try:   
        ssid = sys.argv[1]
        device = sys.argv[2]
        env = Environment(device, ssid, v=True)
    except IndexError:
        print 'Proper usage: python ddrone.py {ssid} {wireless device}'
        
    if env:
        env.crackdrone(0)
        

if __name__ == '__main__':
    main()
