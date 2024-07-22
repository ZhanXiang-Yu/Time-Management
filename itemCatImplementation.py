"""
implement sort when initialize
replace all searches to more time-efficeint search algo on sorted lists of dict.
"""

from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

import csv


class ItemCatClass:
    def __init__(self, parent):
        #hold parent arg.
        self.parent = parent
        
        #stringVar for UI in popup
        self.itemUI = StringVar()
        self.catUI = StringVar()
        self.warning = StringVar()
        
        #boolVar for dynamic loading
        self.isCat = BooleanVar()
        self.isCat.set(False)
        self.isItem = BooleanVar()
        self.isItem.set(False)
        
        #associate callback of dynamic loading to boolVars
        self.isCat.trace_add("write", self.menuFill)
        self.isItem.trace_add("write", self.menuFill)
        
        
        #load cat. image
        self.catImg = ImageTk.PhotoImage(Image.open("tags.png"))
        
        #load item image
        self.itemImg = ImageTk.PhotoImage(Image.open("note.png"))
        
        #load add New/delete image
        self.editImg = ImageTk.PhotoImage(Image.open("plus.png"))
        
        #load delete mark image
        self.deleteMark = ImageTk.PhotoImage(Image.open("delete.png"))
        
        #init. dict.
        self.itemsCats = {}
        
        #populate lists
        self.read()
        
        #description of curr. selected item/cat for display
        self.itemCatDescription = StringVar()
        self.itemCatDescription.set("item unselected / cat. unselected")
        
        #item/cat frame
        self.itemCatWidget = ttk.Frame(parent, padding="3 3 12 12")
        self.itemCatWidget.grid(row=1, column=1, sticky="nw")
        
        #frame for item/item dropdown, and cat/cat dropdown
        self.itemSelect = ttk.Frame(self.itemCatWidget, padding="3 3 12 12")
        self.itemSelect.grid(row=0, column=1, sticky="e")
        self.catSelect = ttk.Frame(self.itemCatWidget, padding="3 3 12 12")
        self.catSelect.grid(row=0, column=2, sticky="e")
        
        #item description/select widget
        self.itemButton = ttk.Button(self.itemSelect, image=self.itemImg)
        self.itemButton.grid(row=0, column=0)
        #bind to event
        self.itemButton.bind("<ButtonRelease-1>", self.showItems)
        
        #cat description/select widget
        self.catButton = ttk.Button(self.catSelect, image=self.catImg)
        self.catButton.grid(row=0, column=0)
        #bind to event
        self.catButton.bind("<ButtonRelease-1>", self.showCats)
        
        #create dropdown menu widget
        self.itemDropdown = Menu(self.itemSelect)
        self.itemDropdown.grid_forget()
        self.catDropdown = Menu(self.catSelect)
        self.catDropdown.grid_forget()
        
        self.displayFrame = ttk.Frame(parent, padding="3 3 12 12")
        self.displayFrame.grid(row=1, column=0, sticky="w", padx=(0,30))
        #string display widget create
        self.display = ttk.Label(self.displayFrame, textvariable=self.itemCatDescription)
        self.display.grid(row=0, column=0, sticky="nw")
        
        #fill menus
        self.menuFill()

        #create button for edit popup menu
        self.editSelect = ttk.Frame(self.itemCatWidget, padding="3 3 12 12")
        self.editSelect.grid(row=0, column=3, sticky="e")
        self.edit = ttk.Button(self.editSelect, image=self.editImg, command=self.popupCreate)
        self.edit.pack()
        
        
        #constructor testing
        #self.printAll()
    
    def read(self): #load items/cats to instance of class attirbutes lists and dict.
        cats = []
        items = []
        with open("itemCatList.csv", "r", newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    cats.append(row[0])
                    row.pop(0)
                    items.append(row)
        #make into dict.
        self.itemsCats = dict(zip(cats, items)) #{cat1 : [items of cat1], ...}
    
    def printAll(self): #print everything
        print(self.itemsCats.keys())
        print(len(self.itemsCats.keys()))
        print("\n")
        print(self.itemsCats.items())
        print(len(self.itemsCats.items()))
        print("\n")
        print(self.itemsCats)
        print("\n")

    def menuFill(self, traceReturnVal1 = None, traceReturnVal2 = None, traceReturnVal3 = None,): #add command for elem in cats/items list
        #clear menu first
        self.itemDropdown.delete(0, 'end')
        self.catDropdown.delete(0, 'end')
        
        #add unselct for item/cat. dropdown
        self.itemDropdown.add_command(label="item unselected", command=self.itemUnselect)
        self.catDropdown.add_command(label="cat unselected", command=self.catUnselect)
        
        #partition curr. string display into item separator cat
        temp = self.itemCatDescription.get()
        tempSeparated = temp.rpartition(" / ")

        #for items computation
        temp = []
        
        #item/cat. unset or both set -> load everything, item set, cat. unset -> load all items, only associated cat.
        if( (self.isCat.get() == True and self.isItem.get() == True) or (self.isCat.get() == False and self.isItem.get() == False) or (self.isCat.get() == False and self.isItem.get() == True)):
            #for cat
            for cat in list(self.itemsCats.keys()):
                #correct reference to obj of each iteration of the loop var to callback func
                self.catDropdown.add_command(label=cat, command=lambda cat = cat : self.showSelectedCat(cat))
            
            #for item
            for item in list(self.itemsCats.values()):
                temp.extend(item)
            for i in temp:
                #correct reference to obj of each iteration of the loop var to callback func
                self.itemDropdown.add_command(label=i, command=lambda i = i : self.showSelectedItem(i))
        
        #cat. set, item unset -> load items of set cat., all cats
        if( self.isCat.get() == True and self.isItem.get() == False):
            for cat in list(self.itemsCats.keys()):
                #correct reference to obj of each iteration of the loop var to callback func
                self.catDropdown.add_command(label=cat, command=lambda cat = cat : self.showSelectedCat(cat))
            
            for item in self.itemsCats.get(tempSeparated[2]):
                self.itemDropdown.add_command(label=item, command=lambda item = item : self.showSelectedItem(item))
        
    def itemUnselect(self):
        self.isItem.set(False)
        self.isCat.set(False)
        self.itemCatDescription.set("item unselected / cat. unselected")
    
    def catUnselect(self):
        self.isItem.set(False)
        self.isCat.set(False)
        self.itemCatDescription.set("item unselected / cat. unselected")

    def showCats(self, event):
        #show cats. menu
        self.catDropdown.tk_popup(event.x_root, event.y_root)
    
    def showItems(self, event):
        #show items menu
        self.itemDropdown.tk_popup(event.x_root, event.y_root)
    
    def showSelectedCat(self, keyword): #as func name shows
        #partition curr. string display into item separator cat
        temp = self.itemCatDescription.get()
        tempSeparated = temp.rpartition(" / ")  
        
        #add selected cat to correct order and set stringVar
        newTemp = tempSeparated[0] + tempSeparated[1] + keyword
        self.itemCatDescription.set(newTemp)
        
        #set boolVar
        self.isCat.set(True)
    
    def showSelectedItem(self, keyword): #as func name shows
        #partition curr. string display into item separator cat
        temp = self.itemCatDescription.get()
        tempSeparated = temp.rpartition(" / ")
        
        #add selected cat to correct order and set stringVar
        newTemp = str(keyword) + tempSeparated[1] + tempSeparated[2]
        self.itemCatDescription.set(newTemp)
        
        #set boolVar
        self.isItem.set(True)

    def popupCreate(self):
        
        #create popup widget for items/cats. edit
        editPopup = Toplevel(self.parent)
        editPopup.title("Edit Item / Cat.")
        editPopup.geometry("500x400")  # Width x Height
        
        treeFrame = ttk.Frame(editPopup)
        treeFrame.grid(row=0, column=0)
        
        # Setup the TreeView
        tree = ttk.Treeview(treeFrame, columns=('Categories', 'Items'), show="headings")
        tree.heading('Categories', text='Categories')
        tree.heading('Items', text='Items')
        
        # Add scrollbars
        scrollbar = ttk.Scrollbar(treeFrame, orient=VERTICAL, command=tree.yview)
        #scrollbar.pack(side=RIGHT, fill=Y)
        scrollbar.grid(row=0, column=1, sticky='ns', rowspan=10)
        tree.configure(yscrollcommand=scrollbar.set)
        
        #add cat. from list to tree
        for cat in list(self.itemsCats.keys()):
            #add items from list to tree
            items = self.itemsCats.get(cat)
            for item in items:
                tree.insert("", "end", iid=item+cat, values=(item, cat))
        
        #layout tree
        tree.grid(row=0, column=0)
        
        #bind events of delete when tree node is clicked
        tree.bind("<ButtonRelease-1>", lambda event, tree = tree : self.editPopupFollowing(tree, event))
        
        #addNew label, entry for UI, and button to confirm
        addNewFrame = ttk.Frame(editPopup)
        addNewFrame.grid(row=1, column=0, sticky="nsew")
        addNewLabelButton = ttk.Button(addNewFrame, text="Create", command=lambda : self.write(tree))
        addNewItemEntry = ttk.Entry(addNewFrame, textvariable=self.itemUI)
        addNewCatEntry = ttk.Entry(addNewFrame, textvariable=self.catUI)
        addNewItemEntry.grid(row=0, column=1)
        addNewCatEntry.grid(row=1, column=1)
        addNewLabelButton.grid(row=2, column=0)
        
        addNewItemLabel = ttk.Label(addNewFrame, text="item", foreground="grey")
        addNewCatLabel = ttk.Label(addNewFrame, text="category", foreground="grey")
        addNewItemLabel.grid(row=0, column=0)
        addNewCatLabel.grid(row=1, column=0)
        
        #warning widgets
        warningFrame = ttk.Frame(editPopup)
        warningFrame.grid(row=3, column=0)
        self.warning.set("")
        
        warningLabel = ttk.Label(warningFrame, textvariable=self.warning)
        warningLabel.grid(row=0, column=0)
    
    
    def editPopupFollowing(self, tree, event):
        #get clicked node details
        itemID = tree.identify_row(event.y)
        itemData = tree.item(itemID)
        itemFields = itemData["values"]
        
        #create popup
        deletePopup = Toplevel(self.parent)
        deletePopup.geometry("70x70")
        
        #create frames for delete
        
        deleteFrame = ttk.Frame(deletePopup)
        
        
        deleteFrame.grid(row=2, column=0)
        
        
        #create buttons for delete
        deleteButton = ttk.Button(deleteFrame, image=self.deleteMark, command=lambda : self.delete(itemFields, itemID, tree, deletePopup))
        deleteButton.grid(row=0, column=0)
        #deleteButton.bind("<ButtonRelease-1>", )
        
    def delete(self, itemFields, itemID, tree, popup):
        #search dict for list of items based on key(cat.)
        if(self.itemsCats.get(itemFields[0]) != None): #input validation
            for i in range( len( ( self.itemsCats.get(itemFields[0]) ) ) ): #delete item
                if( (self.itemsCats.get(itemFields[0])) [i] == itemFields[1]):
                    (self.itemsCats.get(itemFields[0])).pop(i)
                    break
        
        #delete cat. if no item is present
        if( len( ( self.itemsCats.get(itemFields[0]) )) == 0 ):
            self.itemsCats.pop(itemFields[0])
        
        #rewrite csv file for items/cats
        with open("itemCatList.csv", "w", newline="") as f:
            writer = csv.writer(f)
            keys = list(self.itemsCats.keys())
            temp = []
            for key in keys:
                temp.append(key)
                temp.extend(self.itemsCats.get(key))
                #print(temp)
                writer.writerow(temp)
                temp = []
        
        #reload
        self.menuFill()
        
        #delete node in treeview for edit popup
        tree.delete(itemID)
        
        #close popup containing delete button
        popup.destroy()
        
        #testing
        #self.printAll()
        
    
    def write(self, tree):
        #pass user inputs
        itemInput = self.itemUI.get()
        catInput = self.catUI.get()
        
        #input validation of format
        if(len(itemInput) == 0 or len(catInput) == 0):
            self.warning.set("empty item or category")
            return
        if(itemInput == " / " or catInput == " / "):
            self.warning.set("invalid characters of item or category")
            return

        #input validation of file content
        tempItemL = self.itemsCats.get(catInput)
        
        #existing cat.
        if(tempItemL != None): 
            for value in tempItemL:
                
                #existing item
                if(itemInput == value): 
                    self.warning.set("existing entry")
                    return
            
            #existing cat., new item
            self.itemsCats[catInput].append(itemInput)
            self.warning.set("entry added")
            tree.insert("", "end", iid=itemInput+catInput, values=(catInput, itemInput))
        
        #new cat., new item
        else:
            self.itemsCats.update({catInput : [itemInput]})
            self.warning.set("entry added")
            tree.insert("", "end", iid=itemInput+catInput, values=(catInput, itemInput))
        
        #rewrite csv file for items/cats
        with open("itemCatList.csv", "w", newline="") as f:
            writer = csv.writer(f)
            keys = list(self.itemsCats.keys())
            temp = []
            for key in keys:
                temp.append(key)
                temp.extend(self.itemsCats.get(key))
                #print(temp)
                writer.writerow(temp)
                temp = []
        
        #reload
        self.menuFill()
        
        #testing
        #self.printAll()
        
        
            