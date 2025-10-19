from patient import Patient
from doctor import Doctor

from tkinter import *
from tkinter import ttk
from customtkinter import *

user = Doctor()

root = CTk() #application window
root.title("MediLocker")
root.geometry('800x500')
root.configure(fg_color = "#443B81")
root.columnconfigure(0, weight = 1)
root.rowconfigure(0, weight = 1)

def load_mainpage():

    mainFrame = CTkFrame(root) #create frame object
    mainFrame.configure(fg_color = 'transparent', 
                        border_width = 4, 
                        border_color = "#2E294E")
    mainFrame.grid(column = 0, row = 0, sticky = 'NSEW') #place in (0, 0) of parent root, sticky implies to anchor
    mainFrame.grid_configure(padx = 20,
                            pady = 20)
    mainFrame.columnconfigure(0, weight = 1)
    mainFrame.rowconfigure(1, weight = 1)

    helloLabel = CTkLabel(mainFrame, text = 'Welcome.\nSign in to continue.')
    helloLabel.configure(font = ('Libre Caslon Text Regular', 50), 
                        fg_color = 'transparent',
                        text_color = "#FFFFFF")
    helloLabel.grid(column = 0, row = 0, sticky = '')
    helloLabel.grid_configure(pady = 100)

    buttonFrame = CTkFrame(mainFrame)
    buttonFrame.configure(fg_color = 'transparent')
    buttonFrame.grid(column = 0, row = 1, sticky = 'NSEW') 
    buttonFrame.grid_configure(padx = 50, pady = 50)
    buttonFrame.columnconfigure(0, weight = 1)

    loginButton = CTkButton(buttonFrame, text = 'SIGN IN', command = load_signinpage)
    loginButton.configure(font = ('Lexend Giga Regular', 20),
                        fg_color = 'transparent',
                        text_color = '#FFFFFF',
                        hover_color = '#DE9E36',
                        width = 300,
                        height = 50,
                        border_width = 4,
                        border_color = '#DE9E36',
                        corner_radius = 10)
    loginButton.grid(column = 0, row = 0, sticky = 'EW')
    loginButton.grid_configure(pady = 20)

    signupButton = CTkButton(buttonFrame, text = 'CREATE ACCOUNT')
    signupButton.configure(font = ('Lexend Giga Regular', 20),
                        fg_color = 'transparent',
                        text_color = '#FFFFFF',
                        hover_color = '#DE9E36',
                        width = 300,
                        height = 50,
                        border_width = 4,
                        border_color = '#DE9E36',
                        corner_radius = 10)

    signupButton.grid(column = 0, row = 1, sticky = 'EW')
    signupButton.grid_configure(pady = 20)

def load_signinpage():

    signinFrame = CTkFrame(root) #create frame object
    signinFrame.configure(fg_color = 'transparent', 
                        border_width = 4, 
                        border_color = "#2E294E")
    signinFrame.grid(column = 0, row = 0, sticky = 'NSEW') #place in (0, 0) of parent root, sticky implies to anchor
    signinFrame.grid_configure(padx = 20,
                            pady = 20)
    signinFrame.columnconfigure(0, weight = 1)
    signinFrame.rowconfigure(1, weight = 1)
    signinFrame.rowconfigure(1, weight = 1)

    signinLabel = CTkLabel(signinFrame, text = 'Sign in')
    signinLabel.configure(font = ('Libre Caslon Text Regular', 50), 
                        fg_color = 'transparent',
                        text_color = "#FFFFFF")
    signinLabel.grid(column = 0, row = 0, sticky = 'W')
    signinLabel.grid_configure(pady = 50,
                               padx = 50)
    
    fillupFrame = CTkFrame(signinFrame)
    fillupFrame.configure(fg_color = 'transparent')
                        #border_width = 4, 
                        #border_color = "#2E294E")
    fillupFrame.grid(column = 0, row = 1, sticky = 'NSEW') #place in (0, 0) of parent root, sticky implies to anchor
    fillupFrame.grid_configure(padx = 20,
                            pady = 20)

    fillupFrame.columnconfigure(0, minsize = 300)
    fillupFrame.columnconfigure(1, weight = 1)

    userLabel = CTkLabel(fillupFrame, text = 'Username')
    userLabel.configure(font = ('Libre Caslon Text Regular', 25), 
                        fg_color = 'transparent',
                        text_color = "#FFFFFF")
    userLabel.grid(column = 0, row = 0, sticky = 'W')
    userLabel.grid_configure(pady = 20,
                            padx = 30)
    
    userEntry = CTkEntry(fillupFrame, placeholder_text = 'Enter your username...')
    userEntry.configure(font = ('Libre Caslon Text Regular', 20),
                        fg_color = '#2E294E',
                        text_color = '#FFFFFF', 
                        placeholder_text_color = '#DE9E36',
                        width = 300,
                        height = 50,
                        border_width = 4,
                        border_color = '#DE9E36',
                        corner_radius = 10)
    userEntry.grid(column = 1, row = 0, sticky = 'EW')
    userEntry.grid_configure(pady = 20,
                            padx = 20)
    

    passwordLabel = CTkLabel(fillupFrame, text = 'Password')
    passwordLabel.configure(font = ('Libre Caslon Text Regular', 25), 
                        fg_color = 'transparent',
                        text_color = "#FFFFFF")
    passwordLabel.grid(column = 0, row = 1, sticky = 'W')
    passwordLabel.grid_configure(pady = 20,
                                padx = 30)
    
    passwordEntry = CTkEntry(fillupFrame, placeholder_text = 'Enter your password...')
    passwordEntry.configure(font = ('Libre Caslon Text Regular', 20),
                        fg_color = '#2E294E',
                        text_color = '#FFFFFF', 
                        placeholder_text_color = '#DE9E36',
                        width = 300,
                        height = 50,
                        border_width = 4,
                        border_color = '#DE9E36',
                        corner_radius = 10)
    passwordEntry.grid(column = 1, row = 1, sticky = 'EW')
    passwordEntry.grid_configure(pady = 20,
                                 padx = 20)
    
    signinButton = CTkButton(fillupFrame, text = 'SIGN IN', command = lambda: user.login(userEntry.get(), passwordEntry.get()))
    signinButton.configure(font = ('Lexend Giga Regular', 20),
                        fg_color = 'transparent',
                        text_color = '#FFFFFF',
                        hover_color = '#DE9E36',
                        width = 200,
                        height = 50,
                        border_width = 4,
                        border_color = '#DE9E36',
                        corner_radius = 10)
    signinButton.grid(column = 1, row = 3, sticky = 'E')
    signinButton.grid_configure(pady = 20,
                               padx = 20)
    
    signinFrame.lift()


load_mainpage()

root.mainloop()

#print(user.doctorID)