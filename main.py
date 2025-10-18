from patient import Patient
from doctor import Doctor

from tkinter import *
from tkinter import ttk
from customtkinter import *

user = Doctor()

root = CTk() #application window
root.title("CS Project")
root.geometry('800x500')
root.configure(fg_color = "#1D262F")
root.columnconfigure(0, weight = 1)
root.rowconfigure(0, weight = 1)

mainFrame = CTkFrame(root) #create frame object
mainFrame.configure(fg_color = 'transparent', 
                    border_width = 4, 
                    border_color = "#2B3743")
mainFrame.grid(column = 0, row = 0, sticky = 'NSEW') #place in (0, 0) of parent root, sticky implies to anchor
mainFrame.grid_configure(padx = 20,
                        pady = 20)
mainFrame.columnconfigure(0, weight = 1)
mainFrame.rowconfigure(1, weight = 1)

helloLabel = CTkLabel(mainFrame, text = 'Hi Anishwar!')
helloLabel.configure(font = ('Poppins Regular', 50), 
                     fg_color = 'transparent')
helloLabel.grid(column = 0, row = 0, sticky = '')
helloLabel.grid_configure(pady = 100)

buttonFrame = CTkFrame(mainFrame)
buttonFrame.configure(fg_color = 'transparent')
buttonFrame.grid(column = 0, row = 1, sticky = 'NSEW') 
buttonFrame.grid_configure(padx = 50, pady = 50)
buttonFrame.columnconfigure(0, weight = 1)

loginButton = CTkButton(buttonFrame, text = 'LOGIN')
loginButton.configure(font = ('Lexend Giga Regular', 20),
                      fg_color = 'transparent',
                      text_color = '#FFFFFF',
                      hover_color = '#14AE92',
                      width = 300,
                      height = 50,
                      border_width = 4,
                      border_color = '#14AE92',
                      corner_radius = 10)
loginButton.grid(column = 0, row = 0, sticky = 'EW')
loginButton.grid_configure(pady = 20)

signupButton = CTkButton(buttonFrame, text = 'CREATE ACCOUNT')
signupButton.configure(font = ('Lexend Giga Regular', 20),
                      fg_color = 'transparent',
                      text_color = '#FFFFFF',
                      hover_color = '#14AE92',
                      width = 300,
                      height = 50,
                      border_width = 4,
                      border_color = '#14AE92',
                      corner_radius = 10)
signupButton.grid(column = 0, row = 1, sticky = 'EW')
signupButton.grid_configure(pady = 20)

root.mainloop()

#user.login('Pranav Vijay', 'EddyHater123')
#print(user.doctorID)