from ftplib import FTP
import os

def changepsk(psk, ftp):
    
    assert (len(psk) >= 8), 'PSK must be at least 8 characters'
    
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
    
def plantrecoveryimage(ftp):
    
    ftp.storbinary('STOR /DCIM/READ-REWARD-IF-FOUND.jpg', open('./resources/reward-recovery/READ-REWARD-IF-FOUND.jpg', 'rb'))