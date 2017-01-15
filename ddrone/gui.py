from Tkinter import *
from environment import *
import commands


class App:
    
    def __init__(self, master, ddrone):
        
        self.root = master
        self.env = ddrone
        self.attacks = {0:'Crack PSK', 1:'Takeover', 2:'Deauth all', 3:'Gather intel', 4:'Plant recovery image', 5:'Plant DCIM malware', 6:'DJ drone', 7:'Hail Mary'}
        self.selectedattack = None
        
        label_device = Label(master, text='Device:').grid(row=0, column=0, padx=5, pady=5)
        label_ssid = Label(master, text='SSID:').grid(row=1, column=0, padx=5, pady=5)
        self.label_error = Label(master, text='No errors so far. Good job!')
        self.label_error.grid(row=5, columnspan=4, padx=5, pady=5, sticky=W)
        
        devs = self.__getdevs()
        var = StringVar(master)
        if devs: var.set('Select device')
        self.optionmenu_device = OptionMenu(master, var, *devs, command=self.__setdevice)
        self.optionmenu_device.grid(row=0, column=1, padx=5, pady=5, sticky=NSEW)
                
        self.entry_ssid = Entry(master, textvariable=StringVar(master, value='PHANTOM'))
        self.entry_ssid.grid(row=1, column=1, padx=5, pady=5)
        
        self.button_scan = Button(master, text='SCAN', command=self.__scanenv, justify=CENTER)
        self.button_scan.grid(row=2, columnspan=2, padx=5, pady=5, sticky=NSEW)
        
        self.listbox_aps = Listbox(master, selectmode=SINGLE, exportselection=False)
        self.listbox_aps.grid(row=3, rowspan=2, columnspan=2, padx=5, pady=5, sticky=NSEW)
        self.listbox_aps.bind('<<ListboxSelect>>', self.__updateapselection)
        
        self.listbox_attacks = Listbox(master, selectmode=SINGLE)
        self.listbox_attacks.grid(row=1, rowspan=3, column=3, padx=5, pady=5)
        self.listbox_attacks.bind('<<ListboxSelect>>', self.__updateattackdetails)
              
        for attack in self.attacks:
            self.listbox_attacks.insert(END, self.attacks[attack])
        
        self.label_key = Label(master, text='Key: NOT FOUND')
        self.label_key.grid(row=0, column=3, padx=5, pady=10)
        
        self.button_attack = Button(master, text='ATTACK', command=self.__attack, justify=CENTER)
        self.button_attack.grid(row=4, column=3, columnspan=1, padx=5, pady=5, sticky=NSEW)
        
        self.frame_attacks = Frame(master, width=200, height=300, borderwidth=2, relief=GROOVE, background='white')
        self.frame_attacks.grid(row=0, rowspan=5, column=4, padx=5, pady=5)
        
        self.label_attackdetails = Label(self.frame_attacks, text='No attack selected.', width=20)
        self.label_attackdetails.pack(side=TOP)
        
        
    def __getdevs(self):        
        return map(lambda dev: dev.split(' ')[0], filter(lambda line: 'IEEE 802.11' in line, commands.scandevs().split('\n')))
        
        
    def __setdevice(self, d):
        self.env.setdevice(d)
        
        
    def __updateattackdetails(self, event):
        
        choice = self.attacks.keys()[self.attacks.values().index(self.listbox_attacks.get(ANCHOR))]
        functions = [self.__crackpskdetails, self.__takeoverdetails, self.__deauthalldetails,
                     self.__gatherinteldetails, self.__plantrecoveryimagedetails, self.__plantdcimmalwaredetails,
                     self.__djdronedetails, self.__hailmarydetails]
        functions[choice]()
        self.selectedattack = choice
        
        
    def __updateapselection(self, event):
        ap = self.env.getaccesspoint(self.listbox_aps.get(ANCHOR))
        self.label_key['text'] = ('Key: ' + ap.key) if ap.key else 'Key: <NOT FOUND>'
        
        
    def __updateaps(self):
        
        self.listbox_aps.delete(0, END)
        for ap in self.env.accesspoints:
            self.listbox_aps.insert(END, ap.ssid)
            
            
    def __attack(self):
        
        self.button_attack['text'] = 'ATTACKING...'
        Tk.update(self.root)
        
        functions = [self.__crackpsk, None, None,
                     None, None, None,
                     None, None]
        
        attackfunction = functions[self.selectedattack]
        if attackfunction: attackfunction()
        else: self.__updateerror('This attack function has not been implemented yet :(')
        
        self.button_attack['text'] = 'ATTACK'
        
        
    def __updateerror(self, text):
        
        self.label_error['text'] = text
        
        
    def __crackpsk(self):
        
        targets = [0]
        
        key = None
        for target in targets:
            key = self.env.crackdrone(target)
            
        if key: self.label_key['text'] = 'Key: ' + str(key)
        
    def __scanenv(self):
        
        self.button_scan['text'] = 'SCANNING...'
        Tk.update(self.root)
        
        self.env.ssid = self.entry_ssid.get()
        
        accesspoints = None
        try:
            accesspoints = self.env.initialize(self.env.device, self.env.ssid)
            self.__updateaps()
        except ValueError as e:
            self.__updateerror(str(e))
        finally:
            self.button_scan['text'] = 'SCAN'
            
    def __crackpskdetails(self):
        self.label_attackdetails['text'] = "Crack the selected SSID's\nPSK using aircrack-ng."
        
    def __takeoverdetails(self):
        self.label_attackdetails['text'] = "Use aircrack-ng and open\nFTP to change WPA PSK\nand boot the user. (TODO)"
        
    def __deauthalldetails(self):
        self.label_attackdetails['text'] = "Continuously deauth all\nclients besides this one. (TODO)"
        
    def __gatherinteldetails(self):
        self.label_attackdetails['text'] = "Gather significant data\nfrom drone. (TODO)"
        
    def __plantrecoveryimagedetails(self):
        self.label_attackdetails['text'] = "Places a recovery image \n onto camera's SD card to\nreport the drone if found. (TODO)"
        
    def __plantdcimmalwaredetails(self):
        self.label_attackdetails['text'] = "Plants malware onto\ncamera's SD card. (TODO)"
        
    def __djdronedetails(self):
        self.label_attackdetails['text'] = "Blow up other drones with\nflashing LEDs and bleep\nbloop sounds.(TODO)"
        
    def __hailmarydetails(self):
        self.label_attackdetails['text'] = "BEWARE: this will delete\nthe entirety of the targets\nfile system. (TODO)"
        

def main():
    
    root = Tk()
    #root.geometry("900x500+300+300")
    root.title('ddrone by DKE')

    app = App(root, ddrone = Environment())
    
    root.mainloop()

    
if __name__ == '__main__':
    main()