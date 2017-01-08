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
        self.label_error.grid(row=4, columnspan=3, padx=5, pady=5, sticky=W)
        
        devs = self.__getdevs()
        var = StringVar(master)
        if devs: var.set('Select device')
        self.optionmenu_device = OptionMenu(master, var, *devs, command=self.__setdevice)
        self.optionmenu_device.grid(row=0, column=1, padx=5, pady=5, sticky=NSEW)
                
        self.entry_ssid = Entry(master, textvariable=StringVar(master, value='PHANTOM'))
        self.entry_ssid.grid(row=1, column=1, padx=5, pady=5)
        
        self.button_scan_text = StringVar(master, value='SCAN')
        self.button_scan = Button(master, text='SCAN', command=self.__scanenv, justify=CENTER)
        self.button_scan.grid(row=2, columnspan=2, padx=5, pady=5, sticky=NSEW)
        
        self.listbox_aps = Listbox(master, selectmode=MULTIPLE)
        self.listbox_aps.grid(row=3, columnspan=2, padx=5, pady=5, sticky=NSEW)
        
        self.frame_attacks = Frame(master, width=300, height=300, background='black')
        self.frame_attacks.grid(row=0, rowspan=4, column=3, padx=5, pady=5)
        
    def __getdevs(self):
        
        return map(lambda dev: dev.split(' ')[0], filter(lambda line: 'IEEE 802.11' in line, commands.scandevs().split('\n')))
        
    def __setdevice(self, d):
        
        self.env.setdevice(d)
        
    def __updateaps(self):
        
        self.listbox_aps.delete(0, END)
        for ap in self.env.accesspoints:
            self.listbox_aps.insert(END, ap.ssid)
        
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
    #root.geometry("300x300+300+300")

    app = App(root, ddrone = Environment())
    
    root.mainloop()

if __name__ == '__main__':
    main()