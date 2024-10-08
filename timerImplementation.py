from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import font


import datetime
import csv

from itemCatImplementation import *

"""
known bugs:
if spam click play/stop button(click the button really fast), as long as it ends on play, the counter increment >1 in 1 sec duration
reason for that is clicking the button is associated with the function pressed which sets the flag for counter logic, multiple instances of the method can be executed
at the same time, and each has its own waiting period of 1 sec, the counterlogic func check flag every one sec, so if the flag ends on true, multiple counter logic runs

solution: fix later, use local varaible, dont use attributes of the obj(probably)
"""

class TimerClass:
    def __init__(self, parent, itemCatInstance, trackingInstance):
        #associate itemCat class instace to this
        self.itemCat = itemCatInstance
        self.tracking = trackingInstance
        
        #set font and font size for counter display
        self.customFont = font.Font(family='Yu Gothic UI', size=90, weight='bold')
        
        #counter display string
        self.counterVal = StringVar()
        #set initial time display format to be 0:0:0
        self.counterVal.set("00:00:00")
        
        #currtime for logging
        self.now = None
        
        #counter related vars
        self.timeSec = 0
        self.timeMin = 0
        self.timeHr = 0
        
        #flags for buttons pressed
        self.pressedFlag = BooleanVar()
        
        #button images of play/stop, pathlist, pathlist index, and list
        self.imgLIndex = 0
        self.imgLPath = ["startPlayButton.png", "stopPlayButton.png"]
        self.imgL = [ImageTk.PhotoImage(Image.open("startPlayButton.png")), ImageTk.PhotoImage(Image.open("stopPlayButton.png"))]
        
        #set layout/geometry
        #timer widget
        self.timerWidget = ttk.Frame(parent)
        self.timerWidget.pack()
        
        #time counting display in timer widget
        self.counter = ttk.Label(self.timerWidget, textvariable=self.counterVal, font=self.customFont)
        self.counter.grid(row=0, column=0, columnspan=3, sticky="nsew")
        
        #play/stop button in timer widget, init. load play button
        self.button = ttk.Button(self.timerWidget, image=self.imgL[0], command=self.pressed)
        self.button.grid(row=1, column=1)
        
        
        
        #set flags to initially false
        self.pressedFlag.set(False)
    
    #setter for pressPlayFlag when button pressed
    def pressed(self):
        #inc img index
        self.imgLIndex += 1
        
        #index out of bound
        if(self.imgLIndex > 1):
            self.imgLIndex = 0
        
        #print("index: ", self.imgLIndex)
            
        #flags condition, pressed + 1 play == 1, stop == 0
        if(self.imgLIndex == 1): 
            self.pressedFlag.set(True)
            #get current time when button pressed for play
            self.currTime()
            self.timerWidget.after(1000, self.counterLogic)
        if(self.imgLIndex == 0): 
            self.pressedFlag.set(False)
        
        #print("pressed flag: ", self.pressedFlag.get())
        
        #load img with corresponding index  
        self.button.config(image=self.imgL[self.imgLIndex])
        
    
    #counter logic
    def counterLogic(self):
        #stop button resets counter
        if(self.pressedFlag.get() == False):
            self.timeSec = 0
            self.timeMin = 0
            self.timeHr = 0
            
            #log to csv file
            self.logging()
            
            self.counterVal.set("00:00:00")
            self.pressedFlag.set(False)
            #print("terminated \n")
            return
        if(self.pressedFlag.get()):
            
            self.timeSec += 1
            
            #convert display from sec to mins and hrs
            if(self.timeSec == 60):
                self.timeSec = 0
                self.timeMin += 1
            if(self.timeMin == 60):
                self.timeMin = 0
                self.timeHr += 1
            
            self.counterVal.set("{hrs:02}:{mins:02}:{secs:02}".format(hrs = self.timeHr, mins = self.timeMin, secs = self.timeSec))
            #print("running \n")
            self.timerWidget.after(1000, self.counterLogic)

    def currTime(self):
        self.now = datetime.datetime.now().strftime("%Y-%m-%d")
        
    def counterValLogged(self):
        return self.counterVal.get()
    
    def logging(self):
        #log timing with whatever entry
        #partition curr. string display into item separator cat
        entry = self.itemCat.itemCatDescription.get()
        entrySeparated = entry.rpartition(" / ")
        
        #put into list
        row = []
        row.append(entrySeparated[0])
        row.append(entrySeparated[2])
        row.append(self.now)
        row.append(self.counterValLogged())
        with open("tracked.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(row)
        
        self.tracking.dictPopulate()
        self.tracking.treePopulate()



        
                
            
            
            
            
        
        