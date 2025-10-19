from tkinter import *
from tkinter import ttk
from customtkinter import *
from PIL import Image

import manager
from patient import Patient
from doctor import Doctor

current_theme = 'light'

set_default_color_theme("ColorThemes/" + current_theme + "mode.json")

root = CTk() #application window
root.title("MediLocker")
root.geometry('800x500')
root.columnconfigure(0, weight = 1)
root.rowconfigure(0, weight = 1)


def load_mainpage():

    mainFrame = CTkFrame(root) #create frame object
    mainFrame.grid(column = 0, row = 0, sticky = 'NSEW') #place in (0, 0) of parent root, sticky implies to anchor
    mainFrame.grid_configure(padx = 20,
                            pady = 20)
    mainFrame.columnconfigure(0, weight = 1)
    mainFrame.rowconfigure(1, weight = 1)

    helloLabel = CTkLabel(mainFrame, text = 'Welcome.\nSign in to continue.')
    helloLabel.configure(font = ('Libre Caslon Text Regular', 50))
    helloLabel.grid(column = 0, row = 0, sticky = '')
    helloLabel.grid_configure(pady = 100)

    buttonFrame = CTkFrame(mainFrame)
    buttonFrame.configure(border_width = 0)
    buttonFrame.grid(column = 0, row = 1, sticky = 'NSEW') 
    buttonFrame.grid_configure(padx = 50, pady = 50)
    buttonFrame.columnconfigure(0, weight = 1)

    loginButton = CTkButton(buttonFrame, text = 'SIGN IN', command = load_signinpage)
    loginButton.configure(font = ('Lexend Giga Regular', 20),
                        width = 300,
                        height = 50)
    loginButton.grid(column = 0, row = 0, sticky = 'EW')
    loginButton.grid_configure(pady = 20)

    signupButton = CTkButton(buttonFrame, text = 'CREATE ACCOUNT')
    signupButton.configure(font = ('Lexend Giga Regular', 20),
                        width = 300,
                        height = 50)
    signupButton.grid(column = 0, row = 1, sticky = 'EW')
    signupButton.grid_configure(pady = 20)

    mainFrame.lift()

def load_signinpage():

    def on_signin_button_pressed():

        username = userEntry.get()
        password = passwordEntry.get()
        usertype = iamaMenu.get()

        print(usertype)
        if usertype == 'Civilian':
            manager.user = Patient()
        else:
            manager.user = Doctor()

        manager.user.login(username, password)

    signinFrame = CTkFrame(root) #create frame object
    signinFrame.grid(column = 0, row = 0, sticky = 'NSEW') #place in (0, 0) of parent root, sticky implies to anchor
    signinFrame.grid_configure(padx = 20, pady = 20)
    signinFrame.columnconfigure(0, weight = 1)
    signinFrame.rowconfigure(2, weight = 1)

    signinLabel = CTkLabel(signinFrame, text = 'Sign in')
    signinLabel.configure(font = ('Libre Caslon Text Regular', 50))
    signinLabel.grid(column = 0, row = 1, sticky = 'W')
    signinLabel.grid_configure(pady = (20, 20),
                               padx = 50)
    
    exitButton = CTkButton(signinFrame, text = 'BACK', command = load_mainpage)
    exitButtonIcon = CTkImage(Image.open('Icons/' + current_theme + 'backarrow.png'))
    exitButton.configure(font = ('Lexend Giga Regular', 20),
                         fg_color = 'transparent',
                         image = exitButtonIcon,
                         width = 20,
                         height = 20)
    
    exitButton.grid(column = 0, row = 0, sticky = 'W')
    exitButton.grid_configure(pady = (50, 0), padx = 50)

    fillupFrame = CTkFrame(signinFrame)
    fillupFrame.configure(fg_color = 'transparent',
                        border_width = 0)
    fillupFrame.grid(column = 0, row = 2, sticky = 'NSEW') #place in (0, 0) of parent root, sticky implies to anchor
    fillupFrame.grid_configure(padx = 20, pady = 20)
    fillupFrame.columnconfigure(0, minsize = 300)
    fillupFrame.columnconfigure(1, weight = 1)

    iamaLabel = CTkLabel(fillupFrame, text = 'I am a...')
    iamaLabel.configure(font = ('Libre Caslon Text Regular', 25))
    iamaLabel.grid(column = 0, row = 0, sticky = 'W')
    iamaLabel.grid_configure(pady = 10, padx = 30)

    iamaMenu = CTkComboBox(fillupFrame, values = ['Doctor', 'Civilian', 'Clinic'])
    iamaMenu.configure(font = ('Libre Caslon Text Regular', 20), 
                       dropdown_fg_color = "#13315c",
                       dropdown_hover_color = '#527BB7',
                       dropdown_font = ('Libre Caslon Text Regular', 16),
                       dropdown_text_color = '#FFFFFF')
    
    iamaMenu.grid(column = 1, row = 0, sticky = 'EW')
    iamaMenu.grid_configure(pady = 10, padx = 20)

    userLabel = CTkLabel(fillupFrame, text = 'Username')
    userLabel.configure(font = ('Libre Caslon Text Regular', 25))
    userLabel.grid(column = 0, row = 1, sticky = 'W')
    userLabel.grid_configure(pady = 10, padx = 30)
    
    userEntry = CTkEntry(fillupFrame, placeholder_text = 'Enter your username...')
    userEntry.configure(font = ('Libre Caslon Text Regular', 20),
                        width = 300,
                        height = 50)
    userEntry.grid(column = 1, row = 1, sticky = 'EW')
    userEntry.grid_configure(pady = 10, padx = 20)
    userEntry.focus()
    
    passwordLabel = CTkLabel(fillupFrame, text = 'Password')
    passwordLabel.configure(font = ('Libre Caslon Text Regular', 25))
    passwordLabel.grid(column = 0, row = 2, sticky = 'W')
    passwordLabel.grid_configure(pady = 10, padx = 30)
    
    passwordEntry = CTkEntry(fillupFrame, placeholder_text = 'Enter your password...', show = '*')
    passwordEntry.configure(font = ('Libre Caslon Text Regular', 20),
                        width = 300,
                        height = 50)
    passwordEntry.grid(column = 1, row = 2, sticky = 'EW')
    passwordEntry.grid_configure(pady = 10, padx = 20)
    
    signinButton = CTkButton(fillupFrame, text = 'SIGN IN', command = on_signin_button_pressed)
    signinButton.configure(font = ('Lexend Giga Regular', 20),
                        width = 200,
                        height = 50)
    signinButton.grid(column = 1, row = 4, sticky = 'E')
    signinButton.grid_configure(pady = 10, padx = 20)
    
    signinFrame.lift()

    

load_signinpage()

root.mainloop()

#print(user.doctorID)