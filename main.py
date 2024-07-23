"""
add reporting later
"""
from tkinter import *
from tkinter import ttk
import sv_ttk

import timerImplementation
import itemCatImplementation
import trackingImplementation

import sys, os

os.chdir(sys._MEIPASS)

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
            
            self.notebook = ttk.Notebook(self.root)
            self.notebook.pack(expand=True, fill="both")

            #create diff. frames
            self.timerFrame = ttk.Frame(self.notebook, padding="3 3 12 12")
            self.itemCatSelectFrame = ttk.Frame(self.notebook)
            self.trackingFrame = ttk.Frame(self.notebook, padding="3 3 12 12")
            self.editFrame = ttk.Frame(self.notebook, padding="3 3 12 12")
            
            
            #wrap here4
            
            
            #add item/cat select, edit
            self.itemCat = itemCatImplementation.ItemCatClass(self.itemCatSelectFrame, self.editFrame)
            
            #add tracking 
            self.tracking = trackingImplementation.TrackingClass(self.trackingFrame)
            
            #add timer 
            self.timer = timerImplementation.TimerClass(self.timerFrame, self.itemCat, self.tracking)
            
           
            
            
            #add tabs to notebook
            self.notebook.add(self.timerFrame, text="Timer")
            self.notebook.add(self.itemCatSelectFrame, text="Selection")
            self.notebook.add(self.trackingFrame, text="Tracking")
            self.notebook.add(self.editFrame, text="Edit")
            
        
    #start app    
    app = schedulingApp()
    app.root.mainloop()

if __name__ == "__main__":
    main()