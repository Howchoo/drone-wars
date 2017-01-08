from ftplib import FTP
import os

def changepsk(psk, username, password, host='192.168.1.1', directory=os.getcwd()):
    
    ftp = FTP(host, username, password)
    
    # update config files with new PSK
    ftp.cwd('/etc/config/')
    ftp.sendcmd('put wireless_*')
    
    # update boot file with commands to export config files
    ftp.cwd('/etc/init.d/')
    ftp.sendcmd('put rcS')
    
    # trigger system reboot
    ftp.cwd('/proc/')
    ftp.sendcmd('put sysrq-trigger')
    
    ftp.quit()