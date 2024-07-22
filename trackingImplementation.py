"""
add sorting later to be faster
add total time of a entry on a given day
add graphical view
"""

"""
frame -> treeview -> func to populate treeview based on csv
dict. -> key is date, value is item/cat
    first: create key value pair
    second: append values of value(item/cat) to key
    third: print
"""

from tkinter import *
from tkinter import ttk
#from PIL import ImageTk, Image

import csv


class TrackingClass:
    def __init__(self, parent):
        #treeview for tracking
        self.tree = ttk.Treeview(parent, padding="3 3 12 12", columns=("Date", "Category", "Item", "Duration"), show="")
        self.tree.grid(row=2, column=0, columnspan=5, sticky="nswe")

        
        #dict. for printing
        self.dateItemCat = {}
        self.dictPopulate()
        
        #print from csv to tree
        self.treePopulate()
        
        #testing
        #self.printAll()
    
    def printAll(self):
        print(self.dateItemCat)
    
    def dictPopulate(self):
        #temp list to store value
        tempValues = []
        #temp list to store keys
        tempKeys = []
        
        with open("tracked.csv", "r", newline="") as f:
            reader = csv.reader(f)
            #get unique keys into a list
            for line in reader:
                
                #append date if key list is empty
                if(len(tempKeys) == 0):
                    tempKeys.append(line[2])
                    continue
                
                currIndexKeys = len(tempKeys) - 1
                if(tempKeys[currIndexKeys] != line[2]):
                    tempKeys.append(line[2])

            #reset file pointer to beginning        
            f.seek(0)
            keyCounter = 0
            #get unique values of a key into a list
            tempValuesForKey = []
            for line in reader:
                #make item/cat/duration of each line into a tuple of 2
                tempCurrTuple = []
                tempCurrTuple.append(line[0])
                tempCurrTuple.append(line[1])
                tempCurrTuple.append(line[3])
                value = tuple(tempCurrTuple)
                #print(value)
                
                #create a list for repeated values associated with a key
                if(line[2] == tempKeys[keyCounter]): #entries are on the same date
                    tempValuesForKey.append(tuple(value))
                    continue
                
                #next date starting
                keyCounter += 1
                tempValues.append(tempValuesForKey.copy()) #append list of entries of the same date as the value of a key(date)
                tempValuesForKey.clear() #clear temp array
                tempValuesForKey.append(tuple(value)) #append 1st entry of diff date        
        
        #add entries for last date
        tempValues.append(tempValuesForKey)
        
        #reverse list
        tempKeys = list(reversed(tempKeys))
        tempValues = list(reversed(tempValues))
        
        #form dict.
        self.dateItemCat = dict(zip(tempKeys, tempValues))        
    
    def treePopulate(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        keys = list(self.dateItemCat.keys())
        for key in keys:
            self.tree.insert("", "end", values=(key, "", "", ""))
            for i in range(len(self.dateItemCat.get(key))):
                self.tree.insert("", "end", values=("", (self.dateItemCat.get(key))[i][0], (self.dateItemCat.get(key))[i][1], (self.dateItemCat.get(key))[i][2]))
