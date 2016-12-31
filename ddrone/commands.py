import subprocess


def startmon(device):
    """device should already be in monitor mode, but this command will start monitor mode"""
    
    command = ['airmon-ng', 'start', device]
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    out, err = p.communicate()
    return out


def searchssid(device, ssid):
    """search for existence of SSID with device"""
    
    command = 'iw ' + device + ' scan | grep ' + ssid
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    out, err = p.communicate()
    return out


def sniffssid(device, ssid):
    """start sniffing packets of SSID with device"""
    
    cleanfiles('output-', wildcard=True)
    
    command = 'xterm -hold -e "airodump-ng --essid ' + ssid + ' -w output ' + device + '" &'
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    
    return 0


def deauth(device, accesspoint_mac, client_mac, packets=10):
    """send deauthentication packets to client and access point with device"""
    
    command = 'aireplay-ng -0 ' + str(packets) + ' -a ' + accesspoint_mac + ' -c ' + client_mac + ' ' + device
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    out, err = p.communicate()
    return out


def cleanfiles(filename, wildcard=False):
    """remove all files from working directory with given file name"""
    
    command = 'rm ' + filename
    
    if wildcard:
        command += '*'
        
    subprocess.Popen(command, shell=True)