from Tkinter import *
from environment import *

class App:
    
    def __init__(self, master, ddrone):
        
        master.title = 'ddrone GUI'
        
        leftcolumn = None
        ssid_row = None
        device_row = None
        
        rightcolumn = None
        
        self.__generatelayout(master)
        
        self.optionsframe = Frame(master)
        self.ssid_entry = Entry(ssid_row)
        self.optionsframe.pack(side=LEFT)
        
        devices = ('option1', 'option2', 'option3')
        menuvar = StringVar()
        menuvar.set(devices[0])
        self.device_optionmenu = OptionMenu(master, menuvar, *devices)
        self.device_optionmenu.pack(side=TOP)
        
    def __generatelayout(self, master):
        
        leftcolumn = Frame(master)
        leftcolumn.pack(side=LEFT)
        
        rightcolumn = Frame(master)
        rightcolumn.pack(side=LEFT)
        
        ssid_row = Frame(leftcolumn)
        ssid_row.pack(side=TOP)
            
        device_row = Frame(leftcolumn)
        device_row.pack(side=TOP)

def main():
    
    root = Tk()
    root.geometry("300x300+300+300")
    root.title = 'ddrone GUI'

    app = App(root, ddrone = Environment())
    
    root.mainloop()

if __name__ == '__main__':
    main()