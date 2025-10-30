from customtkinter import *
from PIL import Image

from datetime import datetime

import manager
from patient import Patient
from doctor import Doctor

#os.startfile('DoctorFiles\DrAk191871\SEMICONDUCTOR.docx')

currentTheme = 'light'
errorColor = '#DB3A34'

if currentTheme == 'light':
    menuColor = '#527bb7'
else:
    menuColor = '#162B3C'

set_default_color_theme("ColorThemes/" + currentTheme + "mode.json")

root = CTk() #application window
root.title("MediLocker")
root.geometry('800x500')
root.columnconfigure(0, weight = 1)
root.rowconfigure(0, weight = 1)

def load_mainpage():

    def on_login_button_pressed():

        mainFrame.destroy()
        load_signinpage()

    def on_signup_button_pressed():

        mainFrame.destroy()
        load_createpage()

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

    loginButton = CTkButton(buttonFrame, text = 'SIGN IN', command = on_login_button_pressed)
    loginButton.configure(font = ('Lexend Giga Regular', 20),
                        width = 300,
                        height = 50)
    loginButton.grid(column = 0, row = 0, sticky = 'EW')
    loginButton.grid_configure(pady = 20)

    signupButton = CTkButton(buttonFrame, text = 'CREATE ACCOUNT', command = on_signup_button_pressed)
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
        errorLabel = CTkLabel(fillupFrame)
        errorLabel.configure(font = ('Libre Caslon Text Bold', 16),
                             text_color = errorColor)

        print(username)
        print(password)           
        if not (username == '' or password == ''):

            if usertype == 'Patient':
                manager.user = Patient()
                manager.userType = 'Patient'

            elif usertype == 'Doctor':
                manager.user = Doctor()
                manager.userType = 'Doctor'

            manager.user.login(username, password)

            if not manager.user.logged_in:

                errorLabel.grid(column = 0, row = 0, sticky = 'W')
                errorLabel.grid_configure(columnspan = 2, pady = 10, padx = 30)
                errorLabel.configure(text = 'The username or password you entered is incorrect. Please try again.')
            
            else:
                
                signinFrame.destroy()
                load_dashboard()

        else:
            errorLabel.grid(column = 0, row = 0, sticky = 'W')
            errorLabel.grid_configure(columnspan = 2, pady = 10, padx = 30)    
            errorLabel.configure(text = 'You need to enter your username and password to continue.')
            
    signinFrame = CTkFrame(root) #create frame object
    signinFrame.grid(column = 0, row = 0, sticky = 'NSEW') #place in (0, 0) of parent root, sticky implies to anchor
    signinFrame.grid_configure(padx = 20, pady = 20)
    signinFrame.columnconfigure(0, weight = 1)
    signinFrame.rowconfigure(2, weight = 1)

    signinLabel = CTkLabel(signinFrame, text = 'Sign in')
    signinLabel.configure(font = ('Libre Caslon Text Regular', 36))
    signinLabel.grid(column = 0, row = 1, sticky = 'W')
    signinLabel.grid_configure(pady = (20, 0),
                               padx = 50)
    
    exitButton = CTkButton(signinFrame, text = 'BACK', command = load_mainpage)
    exitButtonIcon = CTkImage(Image.open('Icons/' + currentTheme + 'backarrow.png'))
    exitButton.configure(font = ('Lexend Giga Regular', 16),
                         fg_color = 'transparent',
                         image = exitButtonIcon,
                         hover = False,
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
    fillupFrame.rowconfigure(0, minsize = 70)

    iamaLabel = CTkLabel(fillupFrame, text = 'I am a...')
    iamaLabel.configure(font = ('Libre Caslon Text Regular', 25))
    iamaLabel.grid(column = 0, row = 1, sticky = 'W')
    iamaLabel.grid_configure(pady = 10, padx = 30)

    iamaMenu = CTkComboBox(fillupFrame, values = ['Doctor', 'Patient', 'Clinic'])
    iamaMenu.configure(font = ('Libre Caslon Text Regular', 20), 
                       dropdown_fg_color = '#FFFFFF',
                       dropdown_hover_color = '#527BB7',
                       dropdown_font = ('Libre Caslon Text Regular', 16),
                       dropdown_text_color = '#10202C')
    iamaMenu.grid(column = 1, row = 1, sticky = 'EW')
    iamaMenu.grid_configure(pady = 10, padx = 20)

    userLabel = CTkLabel(fillupFrame, text = 'Username')
    userLabel.configure(font = ('Libre Caslon Text Regular', 25))
    userLabel.grid(column = 0, row = 2, sticky = 'W')
    userLabel.grid_configure(pady = 10, padx = 30)
    
    userEntry = CTkEntry(fillupFrame, placeholder_text = 'Enter your username...')
    userEntry.configure(font = ('Libre Caslon Text Regular', 20),
                        width = 300,
                        height = 50)
    userEntry.grid(column = 1, row = 2, sticky = 'EW')
    userEntry.grid_configure(pady = 10, padx = 20)
    userEntry.focus()
    
    passwordLabel = CTkLabel(fillupFrame, text = 'Password')
    passwordLabel.configure(font = ('Libre Caslon Text Regular', 25))
    passwordLabel.grid(column = 0, row = 3, sticky = 'W')
    passwordLabel.grid_configure(pady = 10, padx = 30)
    
    passwordEntry = CTkEntry(fillupFrame, placeholder_text = 'Enter your password...', show = '●')
    passwordEntry.configure(font = ('Libre Caslon Text Regular', 20),
                        width = 300,
                        height = 50)
    #passwordEntry.bind('<Return>', command = on_signin_button_pressed)
    passwordEntry.grid(column = 1, row = 3, sticky = 'EW')
    passwordEntry.grid_configure(pady = 10, padx = 20)
    
    signinButton = CTkButton(fillupFrame, text = 'SIGN IN', command = on_signin_button_pressed)
    signinButton.configure(font = ('Lexend Giga Regular', 20),
                        width = 200,
                        height = 50)
    signinButton.grid(column = 1, row = 4, sticky = 'E')
    signinButton.grid_configure(pady = 10, padx = 20)
    
    signinFrame.lift()

def load_createpage():

    def on_create_button_pressed():

        username = userEntry.get()
        password = passwordEntry.get()
        userType = iamaMenu.get()

        if username == '' or password == '':

            print('test')

        else:

            if userType == 'Doctor':
                manager.user = Doctor()
                manager.userType = 'Doctor'


            elif userType == 'Patient':
                manager.user = Patient()
                manager.userType = 'Patient'

            manager.user.signup(username, password)
            createFrame.destroy()
            load_dashboard()

    createFrame = CTkFrame(root) 
    createFrame.grid(column = 0, row = 0, sticky = 'NSEW') 
    createFrame.grid_configure(padx = 20, pady = 20, ipady = 100)
    createFrame.columnconfigure(0, weight = 1)
    createFrame.rowconfigure(2, weight = 1)

    createLabel = CTkLabel(createFrame, text = 'Create an account')
    createLabel.configure(font = ('Libre Caslon Text Regular', 36))
    createLabel.grid(column = 0, row = 1, sticky = 'W') 
    createLabel.grid_configure(pady = (20, 0),
                               padx = 50)
    
    exitButton = CTkButton(createFrame, text = 'BACK', command = load_mainpage)
    exitButtonIcon = CTkImage(Image.open('Icons/' + currentTheme + 'backarrow.png'))
    exitButton.configure(font = ('Lexend Giga Regular', 16),
                         fg_color = 'transparent',
                         image = exitButtonIcon,
                         hover = False,
                         width = 20,
                         height = 20)
    exitButton.grid(column = 0, row = 0, sticky = 'W')
    exitButton.grid_configure(pady = (50, 0), padx = 50)

    fillupFrame = CTkFrame(createFrame)
    fillupFrame.configure(fg_color = 'transparent',
                        border_width = 0)
    fillupFrame.grid(column = 0, row = 2, sticky = 'NSEW') #place in (0, 0) of parent root, sticky implies to anchor
    fillupFrame.grid_configure(padx = 20, pady = (0, 20))
    fillupFrame.columnconfigure(0, minsize = 300)
    fillupFrame.columnconfigure(1, weight = 1)
    fillupFrame.rowconfigure(0, minsize = 70)

    iamaLabel = CTkLabel(fillupFrame, text = 'I am a...')
    iamaLabel.configure(font = ('Libre Caslon Text Regular', 20))
    iamaLabel.grid(column = 0, row = 1, sticky = 'W')
    iamaLabel.grid_configure(pady = 10, padx = 30)

    iamaMenu = CTkComboBox(fillupFrame, values = ['Doctor', 'Patient', 'Clinic'])
    iamaMenu.configure(font = ('Libre Caslon Text Regular', 18), 
                       dropdown_fg_color = '#FFFFFF',
                       dropdown_hover_color = '#527BB7',
                       dropdown_font = ('Libre Caslon Text Regular', 16),
                       dropdown_text_color = '#10202C')
    iamaMenu.grid(column = 1, row = 1, sticky = 'EW')
    iamaMenu.grid_configure(pady = 10, padx = 20)

    userLabel = CTkLabel(fillupFrame, text = 'Create a username: ')
    userLabel.configure(font = ('Libre Caslon Text Regular', 20))
    userLabel.grid(column = 0, row = 2, sticky = 'W')
    userLabel.grid_configure(pady = 10, padx = 30)
   
    userEntry = CTkEntry(fillupFrame, placeholder_text = 'Enter your username... ')
    userEntry.configure(font = ('Libre Caslon Text Regular', 18),
                        width = 300,
                        height = 40)
    userEntry.grid(column = 1, row = 2, sticky = 'EW')
    userEntry.grid_configure(pady = 10, padx = 20)
    userEntry.focus()
    
    passwordLabel = CTkLabel(fillupFrame, text = 'Choose a strong password: ')
    passwordLabel.configure(font = ('Libre Caslon Text Regular', 20))
    passwordLabel.grid(column = 0, row = 3, sticky = 'W')
    passwordLabel.grid_configure(pady = 10, padx = 30)
    
    passwordEntry = CTkEntry(fillupFrame, placeholder_text = 'Enter your password...', show = '●')
    passwordEntry.configure(font = ('Libre Caslon Text Regular', 18),
                        width = 300,
                        height = 40)
    passwordEntry.grid(column = 1, row = 3, sticky = 'EW')
    passwordEntry.grid_configure(pady = 10, padx = 20)

    phonenumLabel = CTkLabel(fillupFrame, text = 'Your phone number: ')
    phonenumLabel.configure(font = ('Libre Caslon Text Regular', 20))
    phonenumLabel.grid(column = 0, row = 4, sticky = 'W')
    phonenumLabel.grid_configure(pady = 10, padx = 30)
    
    phonenumEntry = CTkEntry(fillupFrame, placeholder_text = '91 XXXXXXXXXX')
    phonenumEntry.configure(font = ('Libre Caslon Text Regular', 18),
                        width = 300,
                        height = 40)
    phonenumEntry.grid(column = 1, row = 4, sticky = 'EW')
    phonenumEntry.grid_configure(pady = 10, padx = 20)
    
    createButton = CTkButton(fillupFrame, text = 'CREATE ACCOUNT', command = on_create_button_pressed)
    createButton.configure(font = ('Lexend Giga Regular', 20),
                        width = 200,
                        height = 50)
    createButton.grid(column = 1, row = 5, sticky = 'E')
    createButton.grid_configure(pady = 10, padx = 20)

    createFrame.lift()

def open_menu():

    def on_closemenu_button_pressed():

        menuFrame.destroy()

    def on_menuitem_button_pressed(page):

        menuFrame.destroy()

        if page == 'DASHBOARD':
            load_dashboard() 

        elif page == 'APPOINTMENTS':
            load_appointmentpage()

        elif page == 'ACCOUNT':
            load_accountpage()

        elif page == 'LOGOUT':
            manager.user.logout()
            load_mainpage()

    menuFrame = CTkFrame(root)
    menuFrame.configure(fg_color = menuColor,
                        width = 300,
                        corner_radius = 0,
                        border_width = 0)
    menuFrame.grid(column = 0, row = 0, sticky = 'NSW')

    topFrame = CTkFrame(menuFrame)
    topFrame.configure(border_width = 0)
    topFrame.grid(column = 0, row = 0)
    topFrame.grid_configure(sticky = 'EW')

    closemenuButton = CTkButton(topFrame, text = '', command = on_closemenu_button_pressed)
    closemenuButtonIcon = CTkImage(Image.open('Icons/close.png'), size = (30, 30))    
    closemenuButton.configure(image = closemenuButtonIcon,
                         fg_color = 'transparent',
                         hover = False,
                         width = 50,
                         height = 50)
    closemenuButton.grid(column = 0, row = 0)
    closemenuButton.grid_configure(padx = 20, pady = 20, sticky = 'W')

    menuLabel = CTkLabel(topFrame, text = 'Menu')
    menuLabel.configure(font = ('Libre Caslon Text Regular', 36),
                        text_color = '#FFFFFF')
    menuLabel.grid(column = 1, row = 0, sticky = 'W')
    menuLabel.grid_configure(pady = 20)

    for i, thing in enumerate(['DASHBOARD', 'APPOINTMENTS', 'ACCOUNT', 'LOGOUT']):

        button = CTkButton(menuFrame, text = thing,
                           width = 300, 
                           font = ('Lexend Giga Regular', 16),
                           height = 50,
                           corner_radius = 0,
                           command = lambda x = thing: on_menuitem_button_pressed(x))
        button.grid(column = 0, row = i + 1)
        button.grid_configure(columnspan = 2)

    menuFrame.lift()
    
def load_dashboard():
  
    def on_open_file_pressed(file):

        filePath = os.path.abspath(manager.user.fileDirectory + '/' + file)
        os.startfile(filePath)

    
    dashboardFrame = CTkFrame(root) 
    dashboardFrame.configure(border_width = 0)
    dashboardFrame.grid(column = 0, row = 0, sticky = 'NSEW')
    dashboardFrame.columnconfigure(1, weight = 1)
    dashboardFrame.rowconfigure(1, weight = 1)

    menuButton = CTkButton(dashboardFrame, text = '', command = open_menu)
    menuButtonIcon = CTkImage(Image.open('Icons/' + currentTheme + 'menu.png'), size = (30, 30))    
    menuButton.configure(image = menuButtonIcon,
                         fg_color = 'transparent',
                         hover = False,
                         width = 50,
                         height = 50)
    menuButton.grid(column = 0, row = 0)
    menuButton.grid_configure(padx = 20, pady = 20, sticky = 'W')

    dashboardLabel = CTkLabel(dashboardFrame, text = 'Dashboard')
    dashboardLabel.configure(font = ('Libre Caslon Text Regular', 36))
    dashboardLabel.grid(column = 1, row = 0, sticky = 'W')
    dashboardLabel.grid_configure(pady = 20)

    fileFrame = CTkFrame(dashboardFrame)
    fileFrame.configure(border_width = 0)
    fileFrame.grid(column = 0, row = 1, sticky = 'NSEW')
    fileFrame.grid_configure(columnspan = 2)
    fileFrame.columnconfigure((0, 1, 2), weight = 1)
    fileFrame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight = 1)
    
    current_grid_column = 0
    current_grid_row = 0

    for file in os.listdir(manager.user.fileDirectory):

        fileObject = CTkFrame(fileFrame)
        fileObject.configure(border_width = 2,
                             border_color = "#DF9E25",
                             fg_color = 'transparent',
                             width = 250, 
                            height = 120)
        fileObject.grid(column = current_grid_column, row = current_grid_row)
        fileObject.columnconfigure(0, weight = 1)
        fileObject.grid_propagate(False)

        if current_grid_column == 0:
            fileObject.grid_configure(padx = (20, 5), pady = 10)
        elif current_grid_column == 2:
            fileObject.grid_configure(padx = (5, 20), pady = 10)
        else:
            fileObject.grid_configure(padx = 5, pady = 10)

        fileType = file[:2]
        fileDate = file[3:11]
        fileDoctor = file[12:][:-4]

        if fileType == 'PR':
            fileType = 'Prescription'

        elif fileType == 'MC':
            fileType = 'Medical Certificate'

        elif fileType == 'TR':
            fileType = 'Test Report'
        
        fileTypeLabel = CTkLabel(fileObject, text = fileType)
        fileTypeLabel.configure(font = ('Libre Caslon Text Regular', 12))
        fileTypeLabel.grid(column = 0, row = 0)
        fileTypeLabel.grid_configure(padx = 15, 
                             pady = (5, 0),
                             sticky = 'W')
        
        dateLabel = CTkLabel(fileObject, text = 'Issue Date: ' + fileDate)
        dateLabel.configure(font = ('Libre Caslon Text Regular', 12))
        dateLabel.grid(column = 0, row = 1)
        dateLabel.grid_configure(padx = 15, 
                             pady = 1,
                             sticky = 'W') 
        
        doctLabel = CTkLabel(fileObject, text = 'Issued By: ' + fileDoctor)
        doctLabel.configure(font = ('Libre Caslon Text Regular', 12))
        doctLabel.grid(column = 0, row = 2)
        doctLabel.grid_configure(padx = 15, 
                             pady = 1,
                             sticky = 'W') 

        button = CTkButton(fileObject, text = 'OPEN', command = lambda x = file: on_open_file_pressed(x))
        button.configure(font = ('Lexend Giga Regular', 12))
        button.grid(column = 0, row = 3)
        button.grid_configure(padx = 15,
                              pady = 5,
                              sticky = 'NSWE')
        
        if current_grid_column < 2:
            current_grid_column += 1
        else:
            current_grid_row += 1
            current_grid_column = 0
    
    dashboardFrame.lift()

def load_prescription():

    prescriptionFrame = CTkFrame(root) #create frame object
    prescriptionFrame.grid(column = 0, row = 0, sticky = 'NSEW') #place in (0, 0) of parent root, sticky implies to anchor
    prescriptionFrame.grid_configure(padx = 20, pady = 20)
    prescriptionFrame.columnconfigure(0, weight = 1)
    prescriptionFrame.rowconfigure(2, weight = 1)

    prescriptionLabel = CTkLabel(prescriptionFrame, text = 'Create prescription')
    prescriptionLabel.configure(font = ('Libre Caslon Text Regular', 36))
    prescriptionLabel.grid(column = 0, row = 1, sticky = 'W')
    prescriptionLabel.grid_configure(pady = (20, 0),
                            padx = 50)


    fillupFrame = CTkFrame(prescriptionFrame)
    fillupFrame.configure(fg_color = 'transparent',
                        border_width = 0)
    fillupFrame.grid(column = 0, row = 2, sticky = 'NSEW') #place in (0, 0) of parent root, sticky implies to anchor
    fillupFrame.grid_configure(padx = 20, pady = 20)
    fillupFrame.columnconfigure(0, minsize = 300)
    fillupFrame.columnconfigure(1, weight = 1)
    fillupFrame.rowconfigure(0, minsize = 70)

    medicineLabel = CTkLabel(fillupFrame, text = 'Medicine name:')
    medicineLabel.configure(font = ('Libre Caslon Text Regular', 25))
    medicineLabel.grid(column = 0, row = 2, sticky = 'W')
    medicineLabel.grid_configure(pady = 10, padx = 30)

    medicineEntry = CTkEntry(fillupFrame, placeholder_text = 'Enter medicine name...')
    medicineEntry.configure(font = ('Libre Caslon Text Regular', 20),
                        width = 300,
                        height = 50)
    medicineEntry.grid(column = 1, row = 2, sticky = 'EW')
    medicineEntry.grid_configure(pady = 10, padx = 20)
    medicineEntry.focus()

    dosageLabel = CTkLabel(fillupFrame, text = 'Dosage: ')
    dosageLabel.configure(font = ('Libre Caslon Text Regular', 25))
    dosageLabel.grid(column = 0, row = 3, sticky = 'W')
    dosageLabel.grid_configure(pady = 10, padx = 30)

    dosageEntry= CTkEntry(fillupFrame, placeholder_text = 'Enter quanitity of dosage...')
    dosageEntry.configure(font = ('Libre Caslon Text Regular', 20),
                        width = 300,
                        height = 50)
    dosageEntry.grid(column = 1, row = 3, sticky = 'EW')
    dosageEntry.grid_configure(pady = 10, padx = 20)

    durationLabel = CTkLabel(fillupFrame, text = 'Duration: ')
    durationLabel.configure(font = ('Libre Caslon Text Regular', 25))
    durationLabel.grid(column = 0, row = 4, sticky = 'W')
    durationLabel.grid_configure(pady = 10, padx = 30)

    durationEntry = CTkEntry(fillupFrame, placeholder_text = 'Enter duration of dosage...')
    durationEntry.configure(font = ('Libre Caslon Text Regular', 20),
                        width = 300,
                        height = 50)
    durationEntry.grid(column = 1, row = 4, sticky = 'EW')
    durationEntry.grid_configure(pady = 10, padx = 20)

    frequencyLabel = CTkLabel(fillupFrame, text = 'Frequency: ')
    frequencyLabel.configure(font = ('Libre Caslon Text Regular', 25))
    frequencyLabel.grid(column = 0, row = 5, sticky = 'W')
    frequencyLabel.grid_configure(pady = 10, padx = 30)

    frequencyEntry= CTkEntry(fillupFrame, placeholder_text = 'Enter frequency of dosage...')
    frequencyEntry.configure(font = ('Libre Caslon Text Regular', 20),
                        width = 300,
                        height = 50)
    frequencyEntry.grid(column = 1, row = 5, sticky = 'EW')
    frequencyEntry.grid_configure(pady = 10, padx = 20)

    notesLabel = CTkLabel(fillupFrame, text = 'Notes: ')
    notesLabel.configure(font = ('Libre Caslon Text Regular', 25))
    notesLabel.grid(column = 0, row = 6, sticky = 'W')
    notesLabel.grid_configure(pady = 10, padx = 30)

    notesEntry= CTkEntry(fillupFrame, placeholder_text = 'Additional notes...')
    notesEntry.configure(font = ('Libre Caslon Text Regular', 20),
                        width = 300,
                        height = 50)
    notesEntry.grid(column = 1, row = 6, sticky = 'EW')
    notesEntry.grid_configure(pady = 10, padx = 20)

    addButton = CTkButton(fillupFrame, text = 'Add medicine')
    addButton.configure(font = ('Lexend Giga Regular', 20),
                        width = 200,
                        height = 50)
    addButton.grid(column = 1, row =7, sticky = 'E', command = add_medicine)
    addButton.grid_configure(pady = 10, padx = 20)

    createPrescButton = CTkButton(fillupFrame, text = 'Generate Prescription')
    createPrescButton.configure(font = ('Lexend Giga Regular', 20),
                        width = 200,
                        height = 50)
    createPrescButton.grid(column = 1, row = 9, sticky = 'E', command = generate_prescription)
    createPrescButton.grid_configure(pady = 10, padx = 20)

    def add_medicine():
        medicineName = medicineEntry.get()
        dosage = dosageEntry.get()
        duration = durationEntry.get()
        frequency = frequencyEntry.get()
        notes = notesEntry.get()
        medicine_details = [medicineName, dosage, duration, frequency, notes]
        Doctor.medicines.append(medicine_details)
        medicineEntry.clear(0,END)
        dosageEntry.clear(0,END)
        durationEntry.clear(0,END)
        frequencyEntry.clear(0,END)
        notesEntry.clear(0,END)

    def generate_prescription():
        pass

    prescriptionFrame.lift()


load_mainpage()


root.mainloop()

