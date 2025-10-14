from patient import Patient
from doctor import Doctor

from tkinter import *
from tkinter import ttk

user = Doctor()

def say_hi():
    print('hi')

root = Tk() #application window
root.title("CS Project")

mainframe = ttk.Frame(root, padding = (3, 3, 3, 3)) #create frame object
mainframe.grid(column=0, row=0, sticky=(N, W, E, S)) #place in (0, 0) of parent root, sticky implies to anchor

#ttk.Button(mainframe, text= 'Hi', command= say_hi).grid(column = 1, row = 1, sticky = W)
helloLabel = ttk.Label(mainframe, text = 'Hello, world.', font=('Berlin Sans FB', 32), foreground='#0D2454', relief='flat')
helloLabel.grid(column = 2, row = 1, sticky = N)
helloLabel.grid_configure(padx = 300)

loginButton = ttk.Button(mainframe, text = 'Login', command = say_hi)
loginButton.grid(column = 2, row = 3)
loginButton.configure(width = '50')

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=10, pady=10) #add padding to each item in frame

helloLabel.grid_configure(padx = 150)

root.mainloop()

#user.login('Pranav Vijay', 'EddyHater123')
#print(user.doctorID)