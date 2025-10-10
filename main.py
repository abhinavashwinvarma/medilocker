from app import App
from patient import Patient

from tkinter import *
from tkinter import ttk

user = Patient()


#def say_hi():

  #  name.get()
'''
root = Tk() #application window
root.title("CS Project")
root.configure(bg="#0D2454")

mainframe = ttk.Frame(root, padding = (3, 3, 3, 3)) #create frame object
mainframe.grid(column=0, row=0, sticky=(N, W, E, S)) #place in (0, 0) of parent root, sticky implies to anchor
name = StringVar() #modifiable variable
name_entry = ttk.Entry(mainframe, width = 30, textvariable = name) #fill-up box
name_entry.grid(column = 3, row = 1, sticky = (W, E)) #place in (2, 1) of parent frame

#ttk.Button(mainframe, text= 'Hi', command= say_hi).grid(column = 1, row = 1, sticky = W)
ttk.Label(mainframe, text = 'CS Project.', font=('Berlin Sans FB', 32), background='#0D2454', foreground='White', relief='sunken').grid(column = 2, row = 1, sticky = N)

#ttk.Button(mainframe, text= 'Patient Login', command= user.login).grid(column = 1, row = 1, sticky = W).configure(bg='#0D2454', foreground='White')

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=10, pady=10) #add padding to each item in frame

root.mainloop()
'''

user.login('Anishwar Balaji', 'WallCat')
user.access_files()