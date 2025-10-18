from patient import Patient
from doctor import Doctor

from tkinter import *
from tkinter import ttk
from customtkinter import *

user = Doctor()

def say_hi():
    print('hi')

root = CTk() #application window
root.title("CS Project")
root.configure(fg_color = "#1D262F")
root.geometry('800x500')


mainframe = CTkFrame(root, fg_color = 'transparent') #create frame object
mainframe.grid(column=0, row=0, sticky=(N, W, E, S)) #place in (0, 0) of parent root, sticky implies to anchor

#ttk.Button(mainframe, text= 'Hi', command= say_hi).grid(column = 1, row = 1, sticky = W)
helloLabel = CTkLabel(mainframe, text = 'Hi Anishwar.', font = ('Berlin Sans FB', 48), fg_color="transparent")
helloLabel.grid(column = 2, row = 1, sticky = N)
helloLabel.grid_configure(padx = 300, pady = 30)

login = CTkButton(mainframe, fg_color = "#34FEBB", text = 'LOGIN', text_color = '#1D262F', font = ('Berlin Sans FB', 25), corner_radius = 999)
login.configure(hover_color = "#1EC78F")
login.grid(column = 2, row = 6, sticky = 'N')
root.mainloop()

#user.login('Pranav Vijay', 'EddyHater123')
#print(user.doctorID)