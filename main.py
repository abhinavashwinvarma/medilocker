from customtkinter import *
from PIL import Image, ImageDraw
from tkinter import filedialog
import mysql.connector as sqlx
from math import floor

#User-made modules
import manager
from patient import Patient
from doctor import Doctor

currentTheme = 'dark'
errorColor = '#DB3A34'
scroll = 0

if currentTheme == 'light':
    menuColor = '#527bb7'
    backColor = '#EDF2F5'
    accentColor = '#DF9E25'

else:
    menuColor = '#162B3C'
    backColor = '#0C1821'
    accentColor = '#22BFAC'

set_default_color_theme("ColorThemes/" + currentTheme + "mode.json")

root = CTk() #application window
root.title("MediLocker")
root.geometry('800x500')
root.columnconfigure(0, weight = 1)
root.rowconfigure(0, weight = 1)

doctorUsersQuery = '''CREATE TABLE doctorusers (

                        DoctorID VARCHAR (50),
                        Username VARCHAR (50),
                        Passkey VARCHAR (50),
                        PATIENTS VARCHAR (100));'''
patientUsersQuery = '''CREATE TABLE patientusers (
                        PatientID VARCHAR (50),
                        Username VARCHAR (50),
                        Passkey VARCHAR (50),
                        DOCTORS VARCHAR (100));'''
doctorDetailsQuery = '''CREATE TABLE doctordetails (
                        DoctorID VARCHAR (50),
                        Username VARCHAR (50),
                        Email VARCHAR (50),
                        Phone DECIMAL (10,0), 
                        DOB DATE,
                        Address VARCHAR (50),
                        Qualification VARCHAR(50));'''
patientDetailsQuery = '''CREATE TABLE patientdetails (
                        PatientID VARCHAR (50),
                        Username VARCHAR (50),
                        Email VARCHAR (50),
                        Phone DECIMAL (10,0),
                        Age INT,
                        DOB DATE,
                        Address VARCHAR (50),
                        Conditions VARCHAR(50));'''
appointmentsQuery = '''CREATE TABLE appointments (
                        DoctorID VARCHAR (50),
                        PatientID VARCHAR (50), 
                        AppointmentDate DATE,
                        AppointmentTime TIME,
                        STAT VARCHAR (50),
                        COMPLAINT VARCHAR(100));
                        '''


con = sqlx.connect(user = 'root', password = 'root', host = 'localhost')
cursor = con.cursor()

try: 
    cursor.execute("USE Medicine")
    
except:
    cursor.execute("CREATE DATABASE medicine")
    cursor.execute("USE medicine")

    for query in [doctorUsersQuery, patientUsersQuery, doctorDetailsQuery, patientDetailsQuery, appointmentsQuery]:
        cursor.execute(query)

    con.commit()
    cursor.close()

con.close()

def load_mainpage():

    def on_login_button_pressed():

        mainFrame.destroy()
        load_signinpage()

    def on_signup_button_pressed():

        mainFrame.destroy()
        load_createpage()

    mainFrame = CTkFrame(root) 
    mainFrame.configure(fg_color = 'transparent')
    mainFrame.grid(column = 0, row = 0, sticky = 'NSEW') 
    mainFrame.grid_configure(padx = 20,
                            pady = 20)
    mainFrame.columnconfigure(0, weight = 1)
    mainFrame.rowconfigure(1, weight = 1)

    helloLabel = CTkLabel(mainFrame, text = 'Welcome.\nSign in to continue.')
    helloLabel.configure(font = ('Libre Caslon Text Regular', 42),
                         justify = 'left')
    helloLabel.grid(column = 0, row = 0, sticky = 'W')
    helloLabel.grid_configure(padx = (50, 0), pady = (100, 50))

    buttonFrame = CTkFrame(mainFrame)
    buttonFrame.configure(border_width = 0)
    buttonFrame.grid(column = 0, row = 1, sticky = 'NSEW') 
    buttonFrame.grid_configure(padx = 50, pady = 50)
    buttonFrame.columnconfigure(0, weight = 1)

    loginButton = CTkButton(buttonFrame, text = 'SIGN IN', command = on_login_button_pressed)
    loginButton.configure(font = ('Lexend Giga Regular', 20),
                        width = 100,
                        height = 50)
    loginButton.grid(column = 0, row = 0, sticky = 'EW')
    loginButton.grid_configure(pady = 20)

    signupButton = CTkButton(buttonFrame, text = 'CREATE ACCOUNT', command = on_signup_button_pressed)
    signupButton.configure(font = ('Lexend Giga Regular', 20),
                        width = 100,
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

        #print(username)
        #print(password)           
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

    iamaMenu = CTkComboBox(fillupFrame, values = ['Doctor', 'Patient'])
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

        errorLabel = CTkLabel(fillupFrame)
        errorLabel.configure(font = ('Libre Caslon Text Bold', 16),
                             text_color = errorColor)
        
        username = userEntry.get()
        password = passwordEntry.get()
        usertype = iamaMenu.get()

        if not (username == '' or password == ''):

            if usertype == 'Patient':
                manager.user = Patient()
                manager.userType = 'Patient'

            elif usertype == 'Doctor':
                manager.user = Doctor()
                manager.userType = 'Doctor'

            manager.user.signup(username, password)

            if not manager.user.logged_in:

                errorLabel.grid(column = 0, row = 0, sticky = 'W')
                errorLabel.grid_configure(columnspan = 2, pady = 10, padx = 30)
                errorLabel.configure(text = 'The username or password you entered is incorrect. Please try again.')
            
            else:
                
                createFrame.destroy()
                load_detailspage()

        else:

            errorLabel.grid(column = 0, row = 0, sticky = 'W')
            errorLabel.grid_configure(columnspan = 2, pady = 10, padx = 30)    
            errorLabel.configure(text = 'You need to enter a username and password to continue.')

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

    iamaMenu = CTkComboBox(fillupFrame, values = ['Doctor', 'Patient'])
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
  
    createButton = CTkButton(fillupFrame, text = 'CREATE ACCOUNT', command = on_create_button_pressed)
    createButton.configure(font = ('Lexend Giga Regular', 18),
                        width = 200,
                        height = 50)
    createButton.grid(column = 1, row = 4, sticky = 'E')
    createButton.grid_configure(pady = 10, padx = 20)

    createFrame.lift()

def load_detailspage():

    def on_create_button_pressed():

        errorLabel = CTkLabel(fillupFrame)
        errorLabel.configure(font = ('Libre Caslon Text Bold', 16),
                             text_color = errorColor)
        
        phoneNum = numEntry.get()
        email = emailEntry.get()
        address = addressEntry.get()
        dob = dobEntry.get()
        
        try:
            qualification = qualifiEntry.get()
            
        except:
            age = ageEntry.get()

        if not (phoneNum == '' or email == '' or address == '' or dob == ''):

            if manager.userType == 'Patient':
                manager.user.update_details(email, phoneNum, address, dob, age)

            elif manager.userType == 'Doctor':
                manager.user.update_details(email, phoneNum, address, qualification, dob)
                         
            userFrame.destroy()
            load_dashboard()

        else:

            errorLabel.grid(column = 0, row = 0, sticky = 'W')
            errorLabel.grid_configure(columnspan = 2, pady = 10, padx = 30)    
            errorLabel.configure(text = 'You need to enter your user details.')

    userFrame = CTkFrame(root) 
    userFrame.grid(column = 0, row = 0, sticky = 'NSEW') 
    userFrame.grid_configure(padx = 20, pady = 20, ipady = 100)
    userFrame.columnconfigure(0, weight = 1)
    userFrame.rowconfigure(2, weight = 1)

    userLabel = CTkLabel(userFrame, text = 'User Info')
    userLabel.configure(font = ('Libre Caslon Text Regular', 36))
    userLabel.grid(column = 0, row = 1, sticky = 'W') 
    userLabel.grid_configure(pady = (50, 0), padx = 50)
    
    fillupFrame = CTkFrame(userFrame)
    fillupFrame.configure(fg_color = 'transparent',
                        border_width = 0)
    fillupFrame.grid(column = 0, row = 2, sticky = 'NSEW') #place in (0, 0) of parent root, sticky implies to anchor
    fillupFrame.grid_configure(padx = 20, pady = (0, 20))
    fillupFrame.columnconfigure(0, minsize = 300)
    fillupFrame.columnconfigure(1, weight = 1)
    fillupFrame.rowconfigure(0, minsize = 70)

    numLabel = CTkLabel(fillupFrame, text = 'Phone Number: ')
    numLabel.configure(font = ('Libre Caslon Text Regular', 20))
    numLabel.grid(column = 0, row = 2, sticky = 'W')
    numLabel.grid_configure(pady = 10, padx = 30)
   
    numEntry = CTkEntry(fillupFrame, placeholder_text = '999999999')
    numEntry.configure(font = ('Libre Caslon Text Regular', 18),
                        width = 300,
                        height = 40)
    numEntry.grid(column = 1, row = 2, sticky = 'EW')
    numEntry.grid_configure(pady = 10, padx = 20)
    numEntry.focus()
    
    emailLabel = CTkLabel(fillupFrame, text = 'Email Address: ')
    emailLabel.configure(font = ('Libre Caslon Text Regular', 20))
    emailLabel.grid(column = 0, row = 3, sticky = 'W')
    emailLabel.grid_configure(pady = 10, padx = 30)
    
    emailEntry = CTkEntry(fillupFrame, placeholder_text = 'name@domain.com')
    emailEntry.configure(font = ('Libre Caslon Text Regular', 18),
                        width = 300,
                        height = 40)
    emailEntry.grid(column = 1, row = 3, sticky = 'EW')
    emailEntry.grid_configure(pady = 10, padx = 20)

    addressEntry = CTkLabel(fillupFrame, text = 'Address: ')
    addressEntry.configure(font = ('Libre Caslon Text Regular', 20))
    addressEntry.grid(column = 0, row = 4, sticky = 'W')
    addressEntry.grid_configure(pady = 10, padx = 30)
    
    addressEntry = CTkEntry(fillupFrame, placeholder_text = '221B Baker St.')
    addressEntry.configure(font = ('Libre Caslon Text Regular', 18),
                        width = 300,
                        height = 40)
    addressEntry.grid(column = 1, row = 4, sticky = 'EW')
    addressEntry.grid_configure(pady = 10, padx = 20)

    dobLabel = CTkLabel(fillupFrame, text = 'DOB: ')
    dobLabel.configure(font = ('Libre Caslon Text Regular', 20))
    dobLabel.grid(column = 0, row = 5, sticky = 'W')
    dobLabel.grid_configure(pady = 10, padx = 30)
    
    dobEntry = CTkEntry(fillupFrame, placeholder_text = 'YYYY-MM-DD')
    dobEntry.configure(font = ('Libre Caslon Text Regular', 18),
                        width = 300,
                        height = 40)
    dobEntry.grid(column = 1, row = 5, sticky = 'EW')
    dobEntry.grid_configure(pady = 10, padx = 20)
    
    if manager.userType == 'Doctor':

        qualifiLabel = CTkLabel(fillupFrame, text = 'Qualifications: ')
        qualifiLabel.configure(font = ('Libre Caslon Text Regular', 20))
        qualifiLabel.grid(column = 0, row = 6, sticky = 'W')
        qualifiLabel.grid_configure(pady = 10, padx = 30)
        
        qualifiEntry = CTkEntry(fillupFrame, placeholder_text = 'Eg. MBBS')
        qualifiEntry.configure(font = ('Libre Caslon Text Regular', 18),
                            width = 300,
                            height = 40)
        qualifiEntry.grid(column = 1, row = 6, sticky = 'EW')
        qualifiEntry.grid_configure(pady = 10, padx = 20)

    elif manager.userType == 'Patient':

        ageLabel = CTkLabel(fillupFrame, text = 'Age: ')
        ageLabel.configure(font = ('Libre Caslon Text Regular', 20))
        ageLabel.grid(column = 0, row = 6, sticky = 'W')
        ageLabel.grid_configure(pady = 10, padx = 30)
    
        ageEntry = CTkEntry(fillupFrame, placeholder_text = 'Enter your age...')
        ageEntry.configure(font = ('Libre Caslon Text Regular', 18),
                            width = 300,
                            height = 40)
        ageEntry.grid(column = 1, row = 6, sticky = 'EW')
        ageEntry.grid_configure(pady = 10, padx = 20)

    createButton = CTkButton(fillupFrame, text = 'CREATE ACCOUNT', command = on_create_button_pressed)
    createButton.configure(font = ('Lexend Giga Regular', 18),
                        width = 200,
                        height = 50)
    createButton.grid(column = 1, row = 7, sticky = 'E')
    createButton.grid_configure(pady = 10, padx = 20)

def open_menu():

    def on_closemenu_button_pressed():

        menuFrame.destroy()

    def on_menuitem_button_pressed(page):

        menuFrame.destroy()

        if page == 'DASHBOARD':
            load_dashboard() 

        elif page == 'PRESCRIPTIONS':

            load_prescriptionpage()

        elif page == 'FIND A DOCTOR':

            load_findpage()

        elif page == 'APPOINTMENTS':
            
            if manager.userType == 'Patient':
                 load_appointmentpage()

            else:
                load_doctor_appointmentpage()

        elif page == 'ACCOUNT':
            
            load_accountpage()

        elif page == 'LOGOUT':

            manager.user.logout()
            manager.user = None
            manager.userType = None
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
    closemenuButtonIcon = CTkImage(Image.open('Icons/darkclose.png'), size = (30, 30))    
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

    menuItems = ['DASHBOARD', 'APPOINTMENTS', 'ACCOUNT', 'LOGOUT']

    if manager.userType == 'Doctor':
        menuItems.insert(1, 'PRESCRIPTIONS')

    elif manager.userType == 'Patient':
        menuItems.insert(1, 'FIND A DOCTOR')

    for i, thing in enumerate(menuItems):

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
    dashboardFrame.grid_configure(columnspan = 3)
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

    image_path = ''
    default_image_path = 'UserBioDataFiles/Defaults/DefaultProfilePhoto.jpg'
    save_path = manager.user.bioDirectory + '/ProfilePhoto.png'

    if os.path.exists(save_path):
        image_path = save_path

    else:
        image_path = default_image_path

    accountPicture = Image.open(image_path)
    accountPictureObject = CTkImage(light_image = accountPicture, size = (50,50))
    accountPictureButton = CTkButton(dashboardFrame,width = 0,height = 0, fg_color = 'transparent',text = '', image = accountPictureObject, command = load_accountpage)
    accountPictureButton.grid(column = 2, row = 0, sticky = 'NE')
    accountPictureButton.grid_configure(padx = 20, pady = 20)
    
    fileFrame = CTkFrame(dashboardFrame)
    fileFrame.configure(border_width = 0)
    fileFrame.grid(column = 0, row = 1, sticky = 'NSEW')
    fileFrame.grid_configure(columnspan = 3)
    fileFrame.columnconfigure((0, 1, 2), weight = 1)
    fileFrame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight = 1)
    
    current_grid_column = 0
    current_grid_row = 0

    global scroll
    fileList = os.listdir(manager.user.fileDirectory)
    fileCount = len(fileList)

    def on_right_button_pressed():
        global scroll

        #print(ceil(fileCount/6))
        if (scroll < floor(fileCount / 6)):
            scroll += 1
        else: 
            scroll = 0

        load_dashboard()

    def on_left_button_pressed():
        global scroll
        if scroll > 0:
            scroll -= 1

        else:
            scroll = 0
        load_dashboard()

    print((6*scroll), (6 * scroll)+6)
    for file in fileList[(6 * scroll) : (6 * scroll) + 6]:

        fileObject = CTkFrame(fileFrame)
        fileObject.configure(border_width = 2,
                             fg_color = 'transparent')
        fileObject.grid(column = current_grid_column, row = current_grid_row, sticky = 'NSEW')
        fileObject.columnconfigure(0, weight = 1)
        #fileObject.rowconfigure((0, 1, 2, 3), weight = 1)
        #fileObject.grid_propagate(False)

        if current_grid_column == 0:
            fileObject.grid_configure(padx = (20, 10), pady = 20)
        elif current_grid_column == 2:
            fileObject.grid_configure(padx = (10, 20), pady = 20)
        else:
            fileObject.grid_configure(padx = 10, pady = 20)

        fileType = file[:2]
        fileDate = file[3:11]

        if '.txt' in file:    
            fileDoctor = file[12:][:-4]

        else:
            fileDoctor = file[12:][:-5]

        if manager.userType == 'Doctor':
            fileDoctor = 'Patient' + fileDoctor


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
        
        doctLabel = CTkLabel(fileObject, text = 'Issued: ' + fileDoctor)
        doctLabel.configure(font = ('Libre Caslon Text Regular', 12))
        doctLabel.grid(column = 0, row = 2)
        doctLabel.grid_configure(padx = 15, 
                             pady = 1,
                             sticky = 'W') 

        button = CTkButton(fileObject, text = 'OPEN', command = lambda x = file: on_open_file_pressed(x))
        button.configure(font = ('Lexend Giga Regular', 12))
        button.grid(column = 0, row = 3)
        button.grid_configure(padx = 15,
                              pady = 15,
                              sticky = 'NSWE')
        
        if current_grid_column < 2:
            current_grid_column += 1
        else:
            current_grid_row += 1
            current_grid_column = 0

        if fileCount > 6:
            if scroll != 0:
                leftbutton = CTkButton(dashboardFrame, text = '<', command = on_left_button_pressed)
                leftbutton.grid(column = 0, row = 4, sticky = 'S')
                leftbutton.grid_configure(pady = 20, padx = 20)

            if scroll != floor(fileCount/6):
                rightbutton = CTkButton(dashboardFrame, text = '>', command = on_right_button_pressed)
                rightbutton.grid(column = 2, row = 4, sticky = 'S')
                rightbutton.grid_configure(pady = 20, padx = 20)
            
    dashboardLabel.lift()
    dashboardFrame.lift()

def load_prescriptionpage():

    def add_medicine():
              
        def on_add_medicine_pressed():
            
            medicine_details = (medicineEntry.get(), dosageEntry.get(), durationEntry.get(), frequencyEntry.get(), notesEntry.get())
            manager.medicines.append(medicine_details)
            #print(manager.medicines)
            subRoot.destroy()
            load_prescriptionpage()

        subRoot = CTk()
        subRoot.title('Add new medicine')
        subRoot.geometry('600x350')
        subRoot.columnconfigure(0, weight = 1)
        subRoot.rowconfigure((0, 1, 2, 3, 4), weight = 1)

        medicineLabel = CTkLabel(subRoot, text = 'Medicine Name:')
        medicineLabel.configure(font = ('Libre Caslon Text Regular', 18))
        medicineLabel.grid(column = 0, row = 0, sticky = 'W')
        medicineLabel.grid_configure(pady = (30, 10), padx = 30)

        medicineEntry = CTkEntry(subRoot, placeholder_text = 'Enter medicine name...')
        medicineEntry.configure(font = ('Libre Caslon Text Regular', 16),
                            width = 300,
                            height = 40)
        medicineEntry.grid(column = 1, row = 0, sticky = 'EW')
        medicineEntry.grid_configure(pady = (30, 10), padx = 30)
        medicineEntry.focus()

        dosageLabel = CTkLabel(subRoot, text = 'Dosage: ')
        dosageLabel.configure(font = ('Libre Caslon Text Regular', 18))
        dosageLabel.grid(column = 0, row = 1, sticky = 'W')
        dosageLabel.grid_configure(pady = 10, padx = 30)

        dosageEntry= CTkEntry(subRoot, placeholder_text = 'Enter quanitity of dosage...')
        dosageEntry.configure(font = ('Libre Caslon Text Regular', 16),
                            width = 300,
                            height = 40)
        dosageEntry.grid(column = 1, row = 1, sticky = 'EW')
        dosageEntry.grid_configure(pady = 10, padx = 30)

        durationLabel = CTkLabel(subRoot, text = 'Duration: ')
        durationLabel.configure(font = ('Libre Caslon Text Regular', 18))
        durationLabel.grid(column = 0, row = 2, sticky = 'W')
        durationLabel.grid_configure(pady = 10, padx = 30)

        durationEntry = CTkEntry(subRoot, placeholder_text = 'Enter duration of dosage...')
        durationEntry.configure(font = ('Libre Caslon Text Regular', 16),
                            width = 300,
                            height = 40)
        durationEntry.grid(column = 1, row = 2, sticky = 'EW')
        durationEntry.grid_configure(pady = 10, padx = 30)

        notesLabel = CTkLabel(subRoot, text = 'Notes: ')
        notesLabel.configure(font = ('Libre Caslon Text Regular', 18))
        notesLabel.grid(column = 0, row = 3, sticky = 'W')
        notesLabel.grid_configure(pady = 10, padx = 30)

        notesEntry= CTkEntry(subRoot, placeholder_text = 'Additional notes...')
        notesEntry.configure(font = ('Libre Caslon Text Regular', 16),
                            width = 300,
                            height = 40)
        notesEntry.grid(column = 1, row = 3, sticky = 'EW')
        notesEntry.grid_configure(pady = 10, padx = 30)

        frequencyLabel = CTkLabel(subRoot, text = 'Time: ')
        frequencyLabel.configure(font = ('Libre Caslon Text Regular', 18))
        frequencyLabel.grid(column = 0, row = 4, sticky = 'W')
        frequencyLabel.grid_configure(pady = 10, padx = 30)

        frequencyEntry= CTkEntry(subRoot, placeholder_text = 'Enter frequency of dosage...')
        frequencyEntry.configure(font = ('Libre Caslon Text Regular', 16),
                            width = 300,
                            height = 40)
        frequencyEntry.grid(column = 1, row = 4, sticky = 'EW')
        frequencyEntry.grid_configure(pady = 10, padx = 30)

        addButton = CTkButton(subRoot, text = 'ADD', command = on_add_medicine_pressed)
        addButton.configure(font = ('Lexend Giga Regular', 20))
        addButton.grid(column = 0, row = 5, sticky = 'NSEW')
        addButton.grid_configure(pady = (10, 30), padx = 30, columnspan = 2)

        subRoot.mainloop()

    def generate_prescription():

        name = manager.user.get_id_from_name(patientMenu.get())
        manager.user.share_prescription(name, diagnosisEntry.get(), manager.medicines)
        
        createdLabel = CTkLabel(prescriptionFrame, text = 'Prescription created!')
        createdLabel.configure(font = ('Libre Caslon Text Regular', 36))
        createdLabel.grid(column = 1, row = 10, sticky = 'SEW')
        createdLabel.grid_configure(pady = 20)

        manager.medicines = []
        load_prescriptionpage()

    prescriptionFrame = CTkFrame(root) 
    prescriptionFrame.configure(border_width = 0)
    prescriptionFrame.grid(column = 0, row = 0, sticky = 'NSEW') #place in (0, 0) of parent root, sticky implies to anchor
    prescriptionFrame.columnconfigure(1, weight = 1)
    prescriptionFrame.rowconfigure(2, weight = 1)

    menuButton = CTkButton(prescriptionFrame, text = '', command = open_menu)
    menuButtonIcon = CTkImage(Image.open('Icons/' + currentTheme + 'menu.png'), size = (30, 30))    
    menuButton.configure(image = menuButtonIcon,
                         fg_color = 'transparent',
                         hover = False,
                         width = 50,
                         height = 50)
    menuButton.grid(column = 0, row = 0)
    menuButton.grid_configure(padx = 20, pady = 20, sticky = 'W')

    prescriptionLabel = CTkLabel(prescriptionFrame, text = 'Share Prescription')
    prescriptionLabel.configure(font = ('Libre Caslon Text Regular', 36))
    prescriptionLabel.grid(column = 1, row = 0, sticky = 'W')
    prescriptionLabel.grid_configure(pady = 20)

    fillupFrame = CTkFrame(prescriptionFrame)
    fillupFrame.configure(fg_color = 'transparent',
                        border_width = 0)
    fillupFrame.grid(column = 0, row = 2, sticky = 'NSEW') #place in (0, 0) of parent root, sticky implies to anchor
    fillupFrame.grid_configure(columnspan = 2)
    fillupFrame.columnconfigure(0, minsize = 300)
    fillupFrame.columnconfigure(1, weight = 1)
    fillupFrame.rowconfigure(0, minsize = 70)

    patientLabel = CTkLabel(fillupFrame, text = 'Patient: ')
    patientLabel.configure(font = ('Libre Caslon Text Regular', 18))
    patientLabel.grid(column = 0, row = 1, sticky = 'W')
    patientLabel.grid_configure(pady = 10, padx = 30)

    patientMenu = CTkComboBox(fillupFrame, values = list(manager.user.consulted.values()))
    patientMenu.configure(font = ('Libre Caslon Text Regular', 18), 
                       dropdown_fg_color = '#FFFFFF',
                       dropdown_hover_color = '#527BB7',
                       dropdown_font = ('Libre Caslon Text Regular', 16),
                       dropdown_text_color = '#10202C')
    patientMenu.grid(column = 1, row = 1, sticky = 'EW')
    patientMenu.grid_configure(pady = 10, padx = 20)

    diagnosisLabel = CTkLabel(fillupFrame, text = 'Diagnosis: ')
    diagnosisLabel.configure(font = ('Libre Caslon Text Regular', 18))
    diagnosisLabel.grid(column = 0, row = 2, sticky = 'W')
    diagnosisLabel.grid_configure(pady = 10, padx = 30)

    diagnosisEntry = CTkEntry(fillupFrame, placeholder_text = 'Enter diagnosis...')
    diagnosisEntry.configure(font = ('Libre Caslon Text Regular', 16),
                        width = 300,
                        height = 40)
    diagnosisEntry.grid(column = 1, row = 2, sticky = 'EW')
    diagnosisEntry.grid_configure(pady = 10, padx = 20)
    
    for i, record in enumerate(manager.medicines):

        medicine, dosage, time, duration, notes = record
        
        medDetails = f'Medicine: {medicine} Dosage: {dosage} Time: {time} Duration: {duration} Notes: {notes}'
        medLabel = CTkLabel(fillupFrame, text = medDetails)
        medLabel.configure(font = ('Libre Caslon Text Regular', 16))
        medLabel.grid(column = 0, row = 3 + i, columnspan = 2)
        medLabel.configure(pady = 10, padx = 30)

    addButton = CTkButton(fillupFrame, text = 'ADD MEDICINE', command = add_medicine)
    addButton.configure(font = ('Lexend Giga Regular', 20),
                        width = 200,
                        height = 50)
    addButton.grid(column = 0, row = len(manager.medicines) + 3, sticky = 'WE')
    addButton.grid_configure(pady = (30, 10), padx = 20, columnspan = 2)

    createPrescButton = CTkButton(fillupFrame, text = 'SHARE PRESCRIPTION', command = generate_prescription)
    createPrescButton.configure(font = ('Lexend Giga Regular', 20),
                        width = 200,
                        height = 50)
    createPrescButton.grid(column = 0, row = len(manager.medicines) + 4, sticky = 'WE')
    createPrescButton.grid_configure(pady = 10, padx = 20, columnspan = 2)

    prescriptionFrame.lift()

def load_accountpage():

    accountDetails = manager.user.get_account_details()
    
    username = accountDetails[0]
    email = accountDetails[1]
    phoneNum = accountDetails[2]
    dob = accountDetails[3]
    address = accountDetails[4]

    accountFrame = CTkFrame(root) 
    accountFrame.configure(border_width = 0)
    accountFrame.grid(column = 0, row = 0, sticky = 'NSEW')
    accountFrame.columnconfigure(1, weight = 1)
    accountFrame.rowconfigure(1, weight = 1)

    menuButton = CTkButton(accountFrame, text = '', command = open_menu)
    menuButtonIcon = CTkImage(Image.open('Icons/' + currentTheme + 'menu.png'), size = (30, 30))    
    menuButton.configure(image = menuButtonIcon,
                         fg_color = 'transparent',
                         hover = False,
                         width = 50,
                         height = 50)
    menuButton.grid(column = 0, row = 0)
    menuButton.grid_configure(padx = 20, pady = 20, sticky = 'W')

    accountLabel = CTkLabel(accountFrame, text = 'My Account')
    accountLabel.configure(font = ('Libre Caslon Text Regular', 36))
    accountLabel.grid(column = 1, row = 0, sticky = 'W')
    accountLabel.grid_configure(pady = 20)

    fillupFrame = CTkFrame(accountFrame)
    fillupFrame.configure(fg_color = 'transparent',
                        border_width = 0)
    fillupFrame.grid(column = 0, row = 2, sticky = 'NSEW') 
    fillupFrame.grid_configure(padx = 10, pady = 10, columnspan = 2)
    fillupFrame.columnconfigure(0, minsize = 300)
    fillupFrame.columnconfigure(1, weight = 1)

    default_image_path = 'UserBioDataFiles/Defaults/DefaultProfilePhoto.jpg'

    save_path = manager.user.bioDirectory + '/ProfilePhoto.png'

    if os.path.exists(save_path):
        image_path = save_path

    else:
        image_path = default_image_path

    manager.iconImage = CTkImage(light_image = Image.open(image_path), size=(100,100))

    iconDisplay = CTkLabel(fillupFrame, text = '', image = manager.iconImage)
    iconDisplay.grid(column = 0, row = 1)
    iconDisplay.grid_configure(pady = 10, padx = 30, columnspan = 2)

    idLabel = CTkLabel(fillupFrame, text = f'ID: {manager.user.ID}')
    idLabel.configure(font = ('Libre Caslon Text Regular', 18))
    idLabel.grid(column = 0, row = 0, sticky = 'W')
    idLabel.grid_configure(pady = (10, 5), padx = 30)

    nameLabel = CTkLabel(fillupFrame, text = 'Name:')
    nameLabel.configure(font = ('Libre Caslon Text Regular', 18))
    nameLabel.grid(column = 0, row = 2, sticky = 'W')
    nameLabel.grid_configure(pady = 10, padx = 30)

    nameDisplay = CTkLabel(fillupFrame, text = username)
    nameDisplay.configure(font = ('Libre Caslon Text Regular', 18))
    nameDisplay.grid(column = 1, row = 2, sticky = 'W')
    nameDisplay.grid_configure(pady = 10, padx = 30)

    emailLabel = CTkLabel(fillupFrame, text = 'Email:')
    emailLabel.configure(font = ('Libre Caslon Text Regular', 18))
    emailLabel.grid(column = 0, row = 3, sticky = 'W')
    emailLabel.grid_configure(pady = 10, padx = 30)

    emailDisplay = CTkLabel(fillupFrame, text = email)
    emailDisplay.configure(font = ('Libre Caslon Text Regular', 18))
    emailDisplay.grid(column = 1, row = 3, sticky = 'W')
    emailDisplay.grid_configure(pady = 10, padx = 30)

    phoneLabel = CTkLabel(fillupFrame, text = 'Phone Number: ')
    phoneLabel.configure(font = ('Libre Caslon Text Regular', 18))
    phoneLabel.grid(column = 0, row = 4, sticky = 'W')
    phoneLabel.grid_configure(pady = 10, padx = 30)

    phoneDisplay = CTkLabel(fillupFrame, text = phoneNum)
    phoneDisplay.configure(font = ('Libre Caslon Text Regular', 18))
    phoneDisplay.grid(column = 1, row = 4, sticky = 'W')
    phoneDisplay.grid_configure(pady = 10, padx = 30)
    
    dobLabel = CTkLabel(fillupFrame, text = 'Date Of birth:')
    dobLabel.configure(font = ('Libre Caslon Text Regular', 18))
    dobLabel.grid(column = 0, row = 5, sticky = 'W')
    dobLabel.grid_configure(pady = 10, padx = 30)

    dobDisplay = CTkLabel(fillupFrame, text = dob)
    dobDisplay.configure(font = ('Libre Caslon Text Regular', 18))
    dobDisplay.grid(column = 1, row = 5, sticky = 'W')
    dobDisplay.grid_configure(pady = 10, padx = 30)

    addressLabel = CTkLabel(fillupFrame, text = 'Address: ')
    addressLabel.configure(font = ('Libre Caslon Text Regular', 18))
    addressLabel.grid(column = 0, row = 6, sticky = 'W')
    addressLabel.grid_configure(pady = 10, padx = 30)

    addressDisplay = CTkLabel(fillupFrame, text = address)
    addressDisplay.configure(font = ('Libre Caslon Text Regular', 18))
    addressDisplay.grid(column = 1, row = 6, sticky = 'W')
    addressDisplay.grid_configure(pady = 10, padx = 30)

    def update_details():
        
        subroot = CTkToplevel()
        subroot.geometry('700x800')
        subroot.title('Update Account Details')
        subroot.attributes('-topmost', True)
        subroot.columnconfigure(0, weight = 1)
        subroot.rowconfigure(1, weight = 1)
        
        username = StringVar()
        email = StringVar()
        phoneNum = StringVar()
        dob = StringVar()
        address = StringVar()

        titleLabel = CTkLabel(subroot, text = 'Change Account Details')
        titleLabel.configure(font = ('Libre Caslon Text Regular', 20))
        titleLabel.grid(column = 0, row = 0, sticky = 'N', pady = 20)
        
        sub_frame = CTkScrollableFrame(subroot, border_width = 0)
        sub_frame.grid(column = 0, row = 1, sticky = 'NSEW') 
        sub_frame.columnconfigure(0, minsize = 300)
        sub_frame.rowconfigure(0, minsize = 70)
        sub_frame.rowconfigure(1, weight = 0)
        sub_frame.columnconfigure(1, weight = 1)

        def get_image():

            filepath  = filedialog.askopenfilename(parent = subroot)

            if not filepath:
                return None
            
            save_path = manager.user.bioDirectory + "/ProfilePhoto.png"
            image = Image.open(filepath)
            image.save(save_path)
            manager.iconImage = CTkImage(Image.open(save_path), size = (100,100))
            iconPreview.configure(image = manager.iconImage)

        def set_default_image():

            default_image = Image.open(default_image_path)
            default_image.save(save_path)
            manager.iconImage = CTkImage(light_image = Image.open(default_image_path), size = (150,150))
            iconPreview.configure(image = manager.iconImage)
                
        uploadButton = CTkButton(sub_frame, font = ('Lexend Giga Regular', 16), text = "UPLOAD", command = get_image)
        uploadButton.grid(column = 0, row = 1, pady = 10)

        removeButton = CTkButton(sub_frame, font = ('Lexend Giga Regular', 16), text = "REMOVE", command = set_default_image)
        removeButton.grid(column = 0, row = 2, pady = 10)

        iconPreview = CTkLabel(sub_frame, text = '', image = manager.iconImage)
        iconPreview.grid(column = 1, row = 1, rowspan = 2)
        iconPreview.grid_configure(pady = 10, padx = 30)

        nameLabel = CTkLabel(sub_frame, text = 'Name:')
        nameLabel.configure(font = ('Libre Caslon Text Regular', 18))
        nameLabel.grid(column = 0, row = 3, sticky = 'W')
        nameLabel.grid_configure(pady = 10, padx = 30)

        nameEntry = CTkEntry(sub_frame, placeholder_text = 'Name', textvariable = username)
        nameEntry.configure(font = ('Libre Caslon Text Regular', 16),
                            width = 300,
                            height = 40)
        nameEntry.grid(column = 1, row = 3, sticky = 'EW')
        nameEntry.grid_configure(pady = 10, padx = 30)

        emailLabel = CTkLabel(sub_frame, text = 'Email:')
        emailLabel.configure(font = ('Libre Caslon Text Regular', 18))
        emailLabel.grid(column = 0, row = 4, sticky = 'W')
        emailLabel.grid_configure(pady = 10, padx = 30)

        emailEntry = CTkEntry(sub_frame, placeholder_text = 'Email', textvariable = email)
        emailEntry.configure(font = ('Libre Caslon Text Regular', 16),
                            width = 300,
                            height = 40)
        emailEntry.grid(column = 1, row = 4, sticky = 'EW')
        emailEntry.grid_configure(pady = 10, padx = 30)

        
        phoneLabel = CTkLabel(sub_frame, text = 'Phone Number: ')
        phoneLabel.configure(font = ('Libre Caslon Text Regular', 18))
        phoneLabel.grid(column = 0, row = 5, sticky = 'W')
        phoneLabel.grid_configure(pady = 10, padx = 30)

        phoneEntry = CTkEntry(sub_frame, placeholder_text = '+91 XXXXXXXXXX ', textvariable = phoneNum)
        phoneEntry.configure(font = ('Libre Caslon Text Regular', 16),
                            width = 300,
                            height = 40)
        phoneEntry.grid(column = 1, row = 5, sticky = 'EW')
        phoneEntry.grid_configure(pady = 10, padx = 30)
        

        dobLabel = CTkLabel(sub_frame, text = 'Date Of birth:')
        dobLabel.configure(font = ('Libre Caslon Text Regular', 18))
        dobLabel.grid(column = 0, row = 6, sticky = 'W')
        dobLabel.grid_configure(pady = 10, padx = 30)

        dobEntry= CTkEntry(sub_frame, placeholder_text = 'YYYY-MM-DD', textvariable = dob)
        dobEntry.configure(font = ('Libre Caslon Text Regular', 16),
                            width = 300,
                            height = 40)
        dobEntry.grid(column = 1, row = 6, sticky = 'EW')
        dobEntry.grid_configure(pady = 10, padx = 30)
        
        addressLabel = CTkLabel(sub_frame, text = 'Address: ')
        addressLabel.configure(font = ('Libre Caslon Text Regular', 18))
        addressLabel.grid(column = 0, row = 7, sticky = 'W')
        addressLabel.grid_configure(pady = 10, padx = 30)

        addressEntry = CTkEntry(sub_frame, placeholder_text = 'Enter address', textvariable = address)
        addressEntry.configure(font = ('Libre Caslon Text Regular', 16),
                            width = 300,
                            height = 40)
        addressEntry.grid(column = 1, row = 7, sticky = 'EW')
        addressEntry.grid_configure(pady = 10, padx = 30)
        
        def go_to_next_entry(entry_list, this_index):
            next_index = this_index + 1
            entry_list[next_index].focus()

        entries = []
        for widget in sub_frame.winfo_children():
            if isinstance(widget, CTkEntry):
                entries.append(widget)

        def make_handler(index):
            def handler(event = None):  
                go_to_next_entry(entries, index)
            return handler

        for i, entry in enumerate(entries):
            entry.bind('<Return>', make_handler(i))

        def passwordChangeToggled():

            if checkBoxState.get():
                
                currentPassword.grid(column = 0, row = 11, sticky = 'W')
                currentPassword.grid_configure(pady = 30, padx = 30)

                currentPasswordEntry.grid(column = 1, row = 11, sticky = 'EW')
                currentPasswordEntry.grid_configure(pady = 30)

                newPassword.grid(column = 0, row = 12, sticky = 'W')
                newPassword.grid_configure(pady = (0, 50), padx = 30)

                newPasswordEntry.grid(column = 1, row = 12, sticky = 'EW')
                newPasswordEntry.grid_configure(pady = (0, 50))

            else: 
                currentPassword.grid_remove()
                currentPasswordEntry.grid_remove()
                newPassword.grid_remove()
                newPasswordEntry.grid_remove()

        checkBoxState = BooleanVar(value = False)
        changePasswordBox = CTkCheckBox(sub_frame, font = ('Lexend Giga Regular', 16), text = "Change Password", variable = checkBoxState, command = passwordChangeToggled)
        changePasswordBox.grid(column = 0, row = 10, stick = 'W', padx = 30)

        currentPassword = CTkLabel(sub_frame, text = 'Enter Current Password')
        currentPassword.configure(font = ('Libre Caslon Text Regular', 18))

        currentPassword_value = StringVar()
        currentPasswordEntry = CTkEntry(sub_frame, placeholder_text = 'Current Password', textvariable = currentPassword_value, show = '●')
        currentPasswordEntry.configure(font = ('Libre Caslon Text Regular', 16),
                            width = 300,
                            height = 40)    

        newPassword = CTkLabel(sub_frame, text = 'Enter New Password')
        newPassword.configure(font = ('Libre Caslon Text Regular', 18))    

        newPassword_value = StringVar()

        newPasswordEntry = CTkEntry(sub_frame, placeholder_text = 'New Password', textvariable = newPassword_value, show = '●')
        newPasswordEntry.configure(font = ('Libre Caslon Text Regular', 16),
                            width = 300,
                            height = 40)
        
        def update_db_and_files():
            
            con = sqlx.connect(host = 'localhost', user = 'root', password = 'root', database = 'medicine')
            cursor = con.cursor()

            if manager.userType == 'Patient':
                fields = {
                "Email": email,
                "Phone": phoneNum,
                "DOB": dob,
                "Address": address
                }

            else:
                fields = {
                "Email": email,
                "Phone": phoneNum,
                "DOB": dob,
                "Address": address}
                
            values = {}
            for field_name, field_var in fields.items():
                    
                    values[field_name] = field_var.get()
                    if values[field_name]:
                        query = f"UPDATE {manager.userType}details SET {field_name} = '{values[field_name]}' WHERE {manager.userType}ID = '{manager.user.ID}'"
                        cursor.execute(query)
                        con.commit()

            if username.get():

                query = f"UPDATE {manager.userType}users SET username = '{username.get()}' WHERE {manager.userType}ID = '{manager.user.ID}'"
                cursor.execute(query)
                con.commit()
                
            if checkBoxState.get():

                if currentPassword_value.get() == manager.user.password:
                    password = newPassword_value.get()
                else:
                    errorLabel = CTkLabel(sub_frame,text = 'The username or password you entered is incorrect. Please try again.', text_color = errorColor)
                    errorLabel.configure(font = ('Libre Caslon Text Regular', 18))
                    errorLabel.grid(column = 0, row = 13, sticky = 'W')
                    errorLabel.grid_configure(columnspan = 2, pady = 10, padx = 30)

                query = f"UPDATE {manager.userType}users SET passkey = '{password}' WHERE {manager.userType}ID = '{manager.user.ID}'"
                cursor = con.cursor()
                cursor.execute(query)
                con.commit()
                con.close()

            subroot.destroy()
            accountFrame.destroy()
            load_accountpage()

        savebutton = CTkButton(sub_frame, text = 'Save Changes' ,command = update_db_and_files)
        savebutton.configure(font = ('Lexend Giga Regular', 20),
                        width = 200,
                        height = 50)
        savebutton.grid(column = 1, row = 9, sticky = 'E')
        savebutton.grid_configure(pady = 10, padx = 20)    

    makeChangesButton = CTkButton(fillupFrame, text = 'EDIT', command = update_details)
    makeChangesButton.configure(font = ('Lexend Giga Regular', 20),
                        width = 200,
                        height = 50)
    makeChangesButton.grid(column = 1, row = 7, sticky = 'E')
    makeChangesButton.grid_configure(pady = (0, 80), padx = 30)
    accountFrame.lift()

def load_appointmentpage():

    def alert_popup():

        def on_button_pressed():
            subroot.destroy()
            manager.user.delete_appointments()
            load_appointmentpage()

        #print(record)
        subroot = CTk()
        subroot.geometry('400x200')
        subroot.columnconfigure(0, weight = 1)
        subroot.rowconfigure((0, 1), weight = 1)

        label = CTkLabel(subroot, text = 'Your appointment request was declined.\nPlease book at a different time.')
        label.configure(font = ('Libre Caslon Text Regular', 16))
        label.grid(row = 0, column = 0)
        label.grid_configure(padx = 30, pady = 30)

        button = CTkButton(subroot, text = 'OK', command = on_button_pressed)
        button.configure(font = ('Lexend Giga Regular', 16))
        button.grid(row = 1, column = 0)
        button.grid_configure(padx = 30, pady = 30)
        subroot.mainloop()

    popupRequired = False
    appointmentFrame = CTkFrame(root) 
    appointmentFrame.configure(border_width = 0)
    appointmentFrame.grid(column = 0, row = 0, sticky = 'NSEW')
    appointmentFrame.columnconfigure(1, weight = 1)

    menuButton = CTkButton(appointmentFrame, text = '', command = open_menu)
    menuButtonIcon = CTkImage(Image.open('Icons/' + currentTheme + 'menu.png'), size = (30, 30))    
    menuButton.configure(image = menuButtonIcon,
                         fg_color = 'transparent',
                         hover = False,
                         width = 50,
                         height = 50)
    menuButton.grid(column = 0, row = 0)
    menuButton.grid_configure(padx = 20, pady = 20, sticky = 'W')

    appointmentLabel = CTkLabel(appointmentFrame, text = 'My Appointments')
    appointmentLabel.configure(font = ('Libre Caslon Text Regular', 36))
    appointmentLabel.grid(column = 1, row = 0, sticky = 'NW')
    appointmentLabel.grid_configure(pady = 20)

    count = len(manager.user.get_appointments())
    textLabel = CTkLabel(appointmentFrame, text = f'You have {count} appointment(s) booked.')
    textLabel.configure(font = ('Libre Caslon Text Regular', 20))
    textLabel.grid(column = 0, row = 1, sticky = 'W')
    textLabel.grid_configure(padx = 40, pady = 20, columnspan = 2)

    listFrame = CTkFrame(appointmentFrame)
    listFrame.grid(column = 0, row = 2, sticky = 'NSEW')
    listFrame.grid_configure(padx = 40, pady = 20, columnspan = 2)
    listFrame.configure(border_width = 0)
    listFrame.columnconfigure((0, 1, 2 ,3), weight = 1)

    nameLabel = CTkLabel(listFrame, text = 'Doctor')
    nameLabel.grid(column = 0, row = 0)
    nameLabel.configure(font = ('Libre Caslon Text Regular', 20))
    nameLabel.grid_configure(padx = 10, pady = 10)

    dateLabel = CTkLabel(listFrame, text = 'Date')
    dateLabel.grid(column = 1, row = 0)
    dateLabel.configure(font = ('Libre Caslon Text Regular', 20))
    dateLabel.grid_configure(padx = 10, pady = 10)

    timeLabel = CTkLabel(listFrame, text = 'Time')
    timeLabel.grid(column = 2, row = 0)
    timeLabel.configure(font = ('Libre Caslon Text Regular', 20))
    timeLabel.grid_configure(padx = 10, pady = 10)
        
    statusLabel = CTkLabel(listFrame, text = 'Status')
    statusLabel.grid(column = 3, row = 0)
    statusLabel.configure(font = ('Libre Caslon Text Regular', 20))
    statusLabel.grid_configure(padx = 10, pady = 10)
        
    for i, lineItem in enumerate(manager.user.get_appointments()):

        docName = lineItem[0]
        appointmentDate = lineItem[1]
        appointmentTime = lineItem[2]
        appointmentStatus = lineItem[3]

        nameLabel = CTkLabel(listFrame, text = docName)
        nameLabel.grid(column = 0, row = i+1)
        nameLabel.configure(font = ('Libre Caslon Text Regular', 18))
        nameLabel.grid_configure(padx = 10, pady = 10)

        dateLabel = CTkLabel(listFrame, text = appointmentDate)
        dateLabel.grid(column = 1, row = i+1)
        dateLabel.configure(font = ('Libre Caslon Text Regular', 18))
        dateLabel.grid_configure(padx = 10, pady = 10)

        timeLabel = CTkLabel(listFrame, text = appointmentTime)
        timeLabel.grid(column = 2, row = i+1)
        timeLabel.configure(font = ('Libre Caslon Text Regular', 18))
        timeLabel.grid_configure(padx = 10, pady = 10)
        
        statusLabel = CTkLabel(listFrame, text = appointmentStatus)
        statusLabel.grid(column = 3, row = i+1)
        statusLabel.configure(font = ('Libre Caslon Text Regular', 18))
        statusLabel.grid_configure(padx = 10, pady = 10)

        #print(appointmentStatus)
        if appointmentStatus == 'Request declined':

            popupRequired = True

    bookButton = CTkButton(appointmentFrame, text = '+ BOOK', command = load_bookappointmentpage)
    bookButton.configure(font = ('Lexend Giga Regular', 18))
    bookButton.grid(column = 0, row = 3)
    bookButton.grid_configure(padx = 40, 
                              pady = 20,
                              columnspan = 2,
                              sticky = 'NSEW')
    
    if popupRequired:
        alert_popup()

def load_bookappointmentpage():

    def on_book_button_pressed():

        docName = docMenu.get()
        complaint = complainEntry.get()
        date = dateEntry.get()
        time = timeEntry.get()

        docID = manager.user.get_id_from_name(docName)
        manager.user.schedule_appointment(docID, date, time, complaint)

        appointmentFrame.destroy()
        load_appointmentpage()

    appointmentFrame = CTkFrame(root) 
    appointmentFrame.configure(border_width = 0)
    appointmentFrame.grid(column = 0, row = 0, sticky = 'NSEW')
    appointmentFrame.columnconfigure(1, weight = 1)
    appointmentFrame.rowconfigure(1, minsize = 20)
    menuButton = CTkButton(appointmentFrame, text = '', command = load_appointmentpage)
    menuButtonIcon = CTkImage(Image.open('Icons/' + currentTheme + 'backarrow.png'), size = (20, 20))    
    menuButton.configure(image = menuButtonIcon,
                         fg_color = 'transparent',
                         hover = False,
                         width = 50,
                         height = 50)
    menuButton.grid(column = 0, row = 0)
    menuButton.grid_configure(padx = 20, pady = 20, sticky = 'W')

    appointmentLabel = CTkLabel(appointmentFrame, text = 'Book an Appointment')
    appointmentLabel.configure(font = ('Libre Caslon Text Regular', 36))
    appointmentLabel.grid(column = 1, row = 0, sticky = 'W')
    appointmentLabel.grid_configure(pady = 20)

    fillupFrame = CTkFrame(appointmentFrame)
    fillupFrame.configure(fg_color = 'transparent',
                        border_width = 0)
    fillupFrame.grid(column = 0, row = 2, sticky = 'NSEW') #place in (0, 0) of parent root, sticky implies to anchor
    fillupFrame.grid_configure(columnspan = 2)
    fillupFrame.columnconfigure(0, minsize = 300)
    fillupFrame.columnconfigure(1, weight = 1)

    docLabel = CTkLabel(fillupFrame, text = 'Doctor to consult: ')
    docLabel.configure(font = ('Libre Caslon Text Regular', 18))
    docLabel.grid(column = 0, row = 1, sticky = 'W')
    docLabel.grid_configure(pady = (20, 10), padx = 40)

    docMenu = CTkComboBox(fillupFrame, values = list(manager.user.consulted.values()))
    docMenu.configure(font = ('Libre Caslon Text Regular', 18), 
                       dropdown_fg_color = '#FFFFFF',
                       dropdown_hover_color = '#527BB7',
                       dropdown_font = ('Libre Caslon Text Regular', 16),
                       dropdown_text_color = '#10202C')
    docMenu.grid(column = 1, row = 1, sticky = 'EW')
    docMenu.grid_configure(pady = (20, 10), padx = 20)

    complainLabel = CTkLabel(fillupFrame, text = "What's bothering you? ")
    complainLabel.configure(font = ('Libre Caslon Text Regular', 18))
    complainLabel.grid(column = 0, row = 2, sticky = 'W')
    complainLabel.grid_configure(pady = 10, padx = 40)

    complainEntry = CTkEntry(fillupFrame, placeholder_text = 'Enter your complaints...')
    complainEntry.configure(font = ('Libre Caslon Text Regular', 16),
                        width = 300,
                        height = 40)
    complainEntry.grid(column = 1, row = 2, sticky = 'EW')
    complainEntry.grid_configure(pady = 10, padx = 20)
    complainEntry.focus()

    dateLabel = CTkLabel(fillupFrame, text = 'Choose a date: ')
    dateLabel.configure(font = ('Libre Caslon Text Regular', 18))
    dateLabel.grid(column = 0, row = 4, sticky = 'W')
    dateLabel.grid_configure(pady = 10, padx = 40)

    dateEntry = CTkEntry(fillupFrame, placeholder_text = 'Enter appointment date...')
    dateEntry.configure(font = ('Libre Caslon Text Regular', 16),
                        width = 300,
                        height = 40)
    dateEntry.grid(column = 1, row = 4, sticky = 'EW')
    dateEntry.grid_configure(pady = 10, padx = 20)

    timeLabel = CTkLabel(fillupFrame, text = 'At what time?')
    timeLabel.configure(font = ('Libre Caslon Text Regular', 18))
    timeLabel.grid(column = 0, row = 5, sticky = 'W')
    timeLabel.grid_configure(pady = 10, padx = 40)

    timeEntry= CTkEntry(fillupFrame, placeholder_text = 'Enter appointment time...')
    timeEntry.configure(font = ('Libre Caslon Text Regular', 16),
                        width = 300,
                        height = 40)
    timeEntry.grid(column = 1, row = 5, sticky = 'EW')
    timeEntry.grid_configure(pady = 10, padx = 20)

    bookButton = CTkButton(fillupFrame, text = '+ BOOK', command = on_book_button_pressed)
    bookButton.grid(column =  0, row = 7)
    bookButton.configure(font = ('Lexend Giga Regular', 16), height = 40)
    bookButton.grid_configure(sticky = 'NSEW',
                             pady = 20,
                             padx = (40, 20),
                             columnspan = 2)

    appointmentFrame.lift()

def load_doctor_appointmentpage():

    def on_view_button_pressed(record):

        subRoot = CTk()
        subRoot.geometry('400x200')
        label = CTkLabel(subRoot, text = record[-1])
        label.configure(font = ('Libre Caslon Text Regular', 18))
        label.grid_configure(padx = 20, pady = 20)
        label.grid(column = 0, row = 0)
        subRoot.mainloop()

    def on_yes_button_pressed(record):

        manager.user.accept_appointment(record)
        load_doctor_appointmentpage()

    def on_no_button_pressed(record):

        manager.user.reject_appointment(record)
        load_doctor_appointmentpage()

    def on_finish_button_pressed(record):

        manager.user.finish_appointment(record)
        load_doctor_appointmentpage()
        
    appointmentFrame = CTkFrame(root) 
    appointmentFrame.configure(border_width = 0)
    appointmentFrame.grid(column = 0, row = 0, sticky = 'NSEW')
    appointmentFrame.columnconfigure(1, weight = 1)

    menuButton = CTkButton(appointmentFrame, text = '', command = open_menu)
    menuButtonIcon = CTkImage(Image.open('Icons/' + currentTheme + 'menu.png'), size = (30, 30))    
    menuButton.configure(image = menuButtonIcon,
                         fg_color = 'transparent',
                         hover = False,
                         width = 50,
                         height = 50)
    menuButton.grid(column = 0, row = 0)
    menuButton.grid_configure(padx = 20, pady = 20, sticky = 'W')

    appointmentLabel = CTkLabel(appointmentFrame, text = 'Scheduled Appointments')
    appointmentLabel.configure(font = ('Libre Caslon Text Regular', 36))
    appointmentLabel.grid(column = 1, row = 0, sticky = 'NW')
    appointmentLabel.grid_configure(pady = 20)

    count = len(manager.user.get_appointments())
    textLabel = CTkLabel(appointmentFrame, text = f'You have {count} appointment(s) scheduled.')
    textLabel.configure(font = ('Libre Caslon Text Regular', 20))
    textLabel.grid(column = 0, row = 1, sticky = 'W')
    textLabel.grid_configure(padx = 40, pady = 20, columnspan = 2)

    listFrame = CTkFrame(appointmentFrame)
    listFrame.grid(column = 0, row = 2, sticky = 'NSEW')
    listFrame.grid_configure(padx = 40, pady = 20, columnspan = 2)
    listFrame.configure(border_width = 0)
    listFrame.columnconfigure((0, 1, 2, 3, 4, 5), weight = 1)
    listFrame.columnconfigure(0, minsize = 100)

    nameLabel = CTkLabel(listFrame, text = 'Patient')
    nameLabel.grid(column = 0, row = 0)
    nameLabel.configure(font = ('Libre Caslon Text Regular', 20))
    nameLabel.grid_configure(padx = 10, pady = 10)

    dateLabel = CTkLabel(listFrame, text = 'Date')
    dateLabel.grid(column = 1, row = 0)
    dateLabel.configure(font = ('Libre Caslon Text Regular', 20))
    dateLabel.grid_configure(padx = 10, pady = 10)

    timeLabel = CTkLabel(listFrame, text = 'Time')
    timeLabel.grid(column = 2, row = 0)
    timeLabel.configure(font = ('Libre Caslon Text Regular', 20))
    timeLabel.grid_configure(padx = 10, pady = 10)
    
    statusLabel = CTkLabel(listFrame, text = 'Status')
    statusLabel.grid(column = 4, row = 0)
    statusLabel.configure(font = ('Libre Caslon Text Regular', 20))
    statusLabel.grid_configure(padx = 10, pady = 10, columnspan = 2)

    viewButtonIcon = CTkImage(Image.open('Icons/' + currentTheme + 'view.png'), size = (30, 30))    
    yesButtonIcon = CTkImage(Image.open('Icons/' + currentTheme + 'yes.png'), size = (30, 30))    
    noButtonIcon = CTkImage(Image.open('Icons/' + currentTheme + 'close.png'), size = (30, 30))

    for i, lineItem in enumerate(manager.user.get_appointments()):

        docName = lineItem[0]
        appointmentDate = lineItem[1]
        appointmentTime = lineItem[2]

        nameLabel = CTkLabel(listFrame, text = docName)
        nameLabel.grid(column = 0, row = i+1)
        nameLabel.configure(font = ('Libre Caslon Text Regular', 18))
        nameLabel.grid_configure(padx = 10, pady = 10)

        dateLabel = CTkLabel(listFrame, text = appointmentDate)
        dateLabel.grid(column = 1, row = i+1)
        dateLabel.configure(font = ('Libre Caslon Text Regular', 18))
        dateLabel.grid_configure(padx = 10, pady = 10)

        timeLabel = CTkLabel(listFrame, text = appointmentTime)
        timeLabel.grid(column = 2, row = i+1)
        timeLabel.configure(font = ('Libre Caslon Text Regular', 18))
        timeLabel.grid_configure(padx = 10, pady = 10)
        
        viewButton = CTkButton(listFrame, text = 'VIEW', command = lambda x = manager.user.get_appointments()[i]: on_view_button_pressed(x))
        viewButton.grid(column = 3, row = i+1)
        viewButton.configure(font = ('Lexend Giga Regular', 16),
                             image = viewButtonIcon,
                             fg_color = 'transparent')
        viewButton.grid_configure(padx = 30, pady = 10, sticky = 'NSEW')

        if lineItem[3] == 'Pending request': 

            yesButton = CTkButton(listFrame, text = '', command = lambda x = lineItem: on_yes_button_pressed(x))
            yesButton.grid(column = 4, row = i+1)
            yesButton.configure(font =  ('Lexend Giga Regular', 16),
                                image = yesButtonIcon,
                                fg_color = 'transparent',
                                width = 40)
            yesButton.grid_configure(padx = (30, 5), pady = 10, sticky = 'NSEW')

            noButton = CTkButton(listFrame, text = '', command = lambda x = lineItem: on_no_button_pressed(x))
            noButton.grid(column = 5, row = i+1)
            noButton.configure(font =  ('Lexend Giga Regular', 16),
                               border_color = accentColor,
                                image = noButtonIcon,
                                fg_color = 'transparent',
                                width = 40)
            noButton.grid_configure(padx = (5, 30), pady = 10, sticky = 'NSEW')

        elif lineItem[3] == 'Confirmed':

            doneButton = CTkButton(listFrame, text = 'FINISH', command = lambda x = lineItem: on_finish_button_pressed(x))
            doneButton.configure(font =  ('Lexend Giga Regular', 16),
                                image = yesButtonIcon,
                                fg_color = 'transparent',
                                width = 40)
            doneButton.grid(column = 5, row = i + 1)
            doneButton.grid_configure(sticky = 'EW')

        else:
            
            confirmLabel = CTkLabel(listFrame, text = 'Declined')
            confirmLabel.grid(column = 4, row = i+1)
            confirmLabel.configure(font = ('Libre Caslon Text Regular', 20))
            confirmLabel.grid_configure(padx = 10, pady = 10, columnspan = 2)

def load_findpage():

    def on_book_button_pressed(doctorID):

        manager.user.add_doctor(doctorID)
        load_findpage()

    findFrame = CTkFrame(root) 
    findFrame.configure(border_width = 0)
    findFrame.grid(column = 0, row = 0, sticky = 'NSEW')
    findFrame.columnconfigure(1, weight = 1)
    findFrame.rowconfigure(1, weight = 1)

    menuButton = CTkButton(findFrame, text = '', command = open_menu)
    menuButtonIcon = CTkImage(Image.open('Icons/' + currentTheme + 'menu.png'), size = (30, 30))    
    menuButton.configure(image = menuButtonIcon,
                         fg_color = 'transparent',
                         hover = False,
                         width = 50,
                         height = 50)
    menuButton.grid(column = 0, row = 0)
    menuButton.grid_configure(padx = 20, pady = 20, sticky = 'W')

    findLabel = CTkLabel(findFrame, text = 'Find a Doctor')
    findLabel.configure(font = ('Libre Caslon Text Regular', 36))
    findLabel.grid(column = 1, row = 0, sticky = 'W')
    findLabel.grid_configure(pady = 20)

    listFrame = CTkFrame(findFrame)
    listFrame.grid(column = 0, row = 1, sticky = 'NSEW')
    listFrame.grid_configure(padx = 40, pady = 20, columnspan = 2)
    listFrame.configure(border_width = 0)
    listFrame.columnconfigure((0, 1, 2 ,3), weight = 1)

    nameLabel = CTkLabel(listFrame, text = 'Name')
    nameLabel.grid(column = 0, row = 0)
    nameLabel.configure(font = ('Libre Caslon Text Regular', 20))
    nameLabel.grid_configure(padx = 10, pady = 10)

    qualiLabel = CTkLabel(listFrame, text = 'Qualifications')
    qualiLabel.grid(column = 1, row = 0)
    qualiLabel.configure(font = ('Libre Caslon Text Regular', 20))
    qualiLabel.grid_configure(padx = 10, pady = 10)

    addressLabel = CTkLabel(listFrame, text = 'Clinic Address')
    addressLabel.grid(column = 2, row = 0)
    addressLabel.configure(font = ('Libre Caslon Text Regular', 20))
    addressLabel.grid_configure(padx = 10, pady = 10)

    for i, record in enumerate(manager.doctors):

        docID = record[0]
        name = record[1]
        qualifications = record[2]
        address = record[3] 

        recNameLabel = CTkLabel(listFrame, text = 'Dr. ' + name)
        recNameLabel.grid(column = 0, row = i + 1)
        recNameLabel.configure(font = ('Libre Caslon Text Regular', 20))
        recNameLabel.grid_configure(padx = 10, pady = 10)

        qualiLabel = CTkLabel(listFrame, text = qualifications)
        qualiLabel.grid(column = 1, row = i + 1)
        qualiLabel.configure(font = ('Libre Caslon Text Regular', 20))
        qualiLabel.grid_configure(padx = 10, pady = 10)

        addressLabel = CTkLabel(listFrame, text = address)
        addressLabel.grid(column = 2, row = i + 1)
        addressLabel.configure(font = ('Libre Caslon Text Regular', 20))
        addressLabel.grid_configure(padx = 10, pady = 10)

        if docID in list(manager.user.consulted.keys()):

            bookLabel = CTkLabel(listFrame, text = 'Booked')
            bookLabel.grid(column = 3, row = i + 1)
            bookLabel.configure(font = ('Libre Caslon Text Regular', 20))
            bookLabel.grid_configure(padx = 10, pady = 10)

        else:

            bookButton = CTkButton(listFrame, text = '+ BOOK', command = lambda x = docID: on_book_button_pressed(x))
            bookButton.grid(column = 3, row = i + 1)
            bookButton.configure(font = ('Lexend Giga Regular', 18))
            bookButton.grid_configure(padx = 10, pady = 10)

    findFrame.lift()

def DEBUG(type = 'Doctor'):
    
    if type != 'Doctor':
        manager.user = Patient()
        manager.userType = 'Patient'
        manager.user.login('Anishwar', 'wallcat')

    else:
        manager.user = Doctor()
        manager.userType = 'Doctor'
        manager.user.login('Abhinav', 'abc123')

    load_dashboard()
    
#DEBUG('A')
load_mainpage()
root.mainloop()

