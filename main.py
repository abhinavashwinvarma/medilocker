from app import App
from patient import Patient
from tkinter import *
from tkinter import ttk

def say_hi():

    name.get()

root = Tk() #application window
root.title("CS Project")

mainframe = ttk.Frame(root, padding = (3, 3, 3, 3)) #create frame object
mainframe.grid(column=0, row=0, sticky=(N, W, E, S)) #place in (0, 0) of parent root, sticky implies to anchor


name = StringVar() #modifiable variable
name_entry = ttk.Entry(mainframe, width = 30, textvariable = name) #fill-up box
name_entry.grid(column = 3, row = 1, sticky = (W, E)) #place in (2, 1) of parent frame

ttk.Button(mainframe, text= 'Hi', command= say_hi).grid(column = 1, row = 1, sticky = W)
ttk.Label(mainframe, text = name).grid(column = 2, row = 1, sticky = E)


for child in mainframe.winfo_children(): 
    child.grid_configure(padx=10, pady=10) #add padding to each item in frame

root.mainloop()
