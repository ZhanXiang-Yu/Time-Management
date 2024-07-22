"""
add reporting later
"""
from tkinter import *
from tkinter import ttk
import sv_ttk

import timerImplementation
import itemCatImplementation
import trackingImplementation
#import reportF

def main():
    class schedulingApp:
        def __init__(self):
            self.root = Tk()
            self.root.title("Time Management")
            
            self.root.grid_rowconfigure(0, weight=1)
            self.root.grid_columnconfigure(0, weight=1)
            
            #theme
            sv_ttk.set_theme("dark")
            
            #no tearoff
            self.root.option_add('*tearOff', False)

            #create a mainframe to make things pretty
            self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
            self.mainframe.grid(column=0, row=0, sticky="nw")
            

            for col in range(3):
                self.mainframe.columnconfigure(col, weight=1)
            
            for row in range(3):
                self.mainframe.rowconfigure(row, weight=1)
            
            #wrap here
            #add item/cat display here
            self.itemCat = itemCatImplementation.ItemCatClass(self.mainframe)
            
            #add tracking here
            self.tracking = trackingImplementation.TrackingClass(self.mainframe)
            
            #add timer here
            self.timer = timerImplementation.TimerClass(self.mainframe, self.itemCat, self.tracking)
            
            #add reporting here
            #self.reporting = reportF.Report(self.mainframe)
        
    #start app    
    app = schedulingApp()
    app.root.mainloop()

if __name__ == "__main__":
    main()