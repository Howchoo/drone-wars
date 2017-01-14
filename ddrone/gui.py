from Tkinter import *
from environment import *
import commands


class App:
    
    def __init__(self, master, ddrone):
        
        self.root = master
        self.env = ddrone
        
        label_device = Label(master, text='Device:').grid(row=0, column=0, padx=5, pady=5)
        label_ssid = Label(master, text='SSID:').grid(row=1, column=0, padx=5, pady=5)
        self.label_error = Label(master, text='No errors so far. Good job!')
        self.label_error.grid(row=5, columnspan=3, padx=5, pady=5, sticky=W)
        
        devs = self.__getdevs()
        var = StringVar(master)
        if devs: var.set('Select device')
        self.optionmenu_device = OptionMenu(master, var, *devs, command=self.__setdevice)
        self.optionmenu_device.grid(row=0, column=1, padx=5, pady=5, sticky=NSEW)
                
        self.entry_ssid = Entry(master, textvariable=StringVar(master, value='PHANTOM'))
        self.entry_ssid.grid(row=1, column=1, padx=5, pady=5)
        
        self.button_scan = Button(master, text='SCAN', command=self.__scanenv, justify=CENTER)
        self.button_scan.grid(row=2, columnspan=2, padx=5, pady=5, sticky=NSEW)
        
        self.listbox_aps = Listbox(master, selectmode=MULTIPLE)
        self.listbox_aps.grid(row=3, rowspan=2, columnspan=2, padx=5, pady=5, sticky=NSEW)
        
        self.listbox_attacks = Listbox(master, selectmode=SINGLE)
        self.listbox_attacks.grid(row=1, rowspan=3, column=3, padx=5, pady=5)
        
        attacks = ['Crack PSK', 'Takeover', 'Deauth all', 'Gather intel', 'Plant recovery image', 'Plant DCIM malware', 'DJ drone', 'Hail Mary']
        for attack in attacks:
            self.listbox_attacks.insert(END, attack)
        
        self.label_key = Label(master, text='Key: NOT FOUND').grid(row=0, column=3, padx=5, pady=10)
        
        self.button_attack = Button(master, text='ATTACK', command=self.__attack, justify=CENTER)
        self.button_attack.grid(row=4, column=3, columnspan=1, padx=5, pady=5, sticky=NSEW)
        
        self.frame_attacks = Frame(master, width=200, height=300, borderwidth=2, relief=GROOVE, background='white')
        self.frame_attacks.grid(row=0, rowspan=5, column=4, padx=5, pady=5)       
        
        
    def __deauth(self):
        
        print 'DEAUTH'
        
        
    def __getdevs(self):
        
        return map(lambda dev: dev.split(' ')[0], filter(lambda line: 'IEEE 802.11' in line, commands.scandevs().split('\n')))
        
        
    def __setdevice(self, d):
        
        self.env.setdevice(d)
        
        
    def __updateaps(self):
        
        self.listbox_aps.delete(0, END)
        for ap in self.env.accesspoints:
            self.listbox_aps.insert(END, ap.ssid)
            
            
    def __attack(self):
        
        self.button_attack["text"] = 'ATTACKING...'
        Tk.update(self.root)
        
        self.__crackpsk()
        
        self.button_attack["text"] = 'ATTACK'
            
            
    def __crackpsk(self):
        
        targets = [0]
        
        for target in targets:
            self.env.crackdrone(target)
            
        
    def __scanenv(self):
        
        self.button_scan["text"] = 'SCANNING...'
        Tk.update(self.root)
        
        self.env.ssid = self.entry_ssid.get()
        
        accesspoints = None
        try:
            accesspoints = self.env.initialize(self.env.device, self.env.ssid)
            self.__updateaps()
        except ValueError as e:
            self.label_error["text"] = str(e)
        finally:
            self.button_scan["text"] = 'SCAN'
        

def main():
    
    root = Tk()
    #root.geometry("900x500+300+300")

    app = App(root, ddrone = Environment())
    
    root.mainloop()

if __name__ == '__main__':
    main()