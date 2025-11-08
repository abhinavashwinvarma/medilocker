import random
import os
import mysql.connector as sqlx
import datetime

class Patient:

    def __init__(self):

        self.logged_in = False
          
    def signup(self, username: str, password: str):
        
        self.username: str = username
        self.password: str = password
        self.ID: str = username[:2] + str(random.randint(100000, 1000000000))
        self.fileDirectory: str = 'PatientFiles/'+ self.ID
        self.consulted = []
        os.mkdir(self.fileDirectory)
        
        con = sqlx.connect(host = 'localhost', user = 'root', password = 'root', database = 'Medicine')
        mycursor = con.cursor()

        query = f"INSERT INTO PatientUsers VALUES ('{self.username}', '{self.password}', '{self.ID}', '{self.consulted}');"

        mycursor.execute(query)
        con.commit()
        con.close()

        #print(query)
        #print('Sign-up success!')

        self.logged_in = True

    def login(self, username, password):

        con = sqlx.connect(host = 'localhost', user = 'root', password = 'root', database = 'Medicine')
        mycursor = con.cursor()
        mycursor.execute('SELECT * FROM PatientUsers;')
                
        for record in mycursor.fetchall():

            if username in record:
                
                correct_password = record[1]

                if password == correct_password:

                    print('Login success!')
                    self.logged_in = True
                    self.username = username
                    self.password = correct_password
                    self.ID = record[-2]
                    self.fileDirectory: str = 'PatientFiles/'+ self.ID
                    self.consulted = eval(record[-1]) 

                    break

                else:

                    print('Incorrect password.')
                    break
            
        if not self.logged_in:
            
            print('This user does not exist.')

        con.close()

    def logout(self):

        self.logged_in = False
        self.username = ''
        self.password = ''
        self.ID = ''

    def access_files(self):

        for file in os.listdir(self.fileDirectory):
            print(file)

    def schedule_appointment(self, doctorID, date, time):

        con = sqlx.connect(host = 'localhost', user = 'root', password = 'root', database = 'medicine')
        query = f'INSERT INTO Appointments VALUES ("{doctorID}", "{self.ID}", "{date}", "{time}");'
        #print(query)
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()
        con.close()

    def get_appointments(self):

        con = sqlx.connect(host = 'localhost', user = 'root', password = 'root', database = 'medicine')
        query = f'SELECT * FROM Appointments WHERE PatientID = "{self.ID}";'
        cursor = con.cursor()
        cursor.execute(query)
        
        data = cursor.fetchall()
        formattedData = []
        
        for thing in data:
            cursor.execute(f'SELECT Username FROM DoctorUsers WHERE DoctorID = "{thing[0]}"')
            docName = cursor.fetchone()[0]
            appointmentDate = thing[2]
            appointmentTime = thing[3]
            appointmentStatus = bool(int(thing[-1]))

            if not appointmentStatus:
                appointmentStatus = 'Pending request'

            else:
                appointmentStatus = 'Confirmed'

            formattedData.append([docName, appointmentDate, appointmentTime, appointmentStatus])

        con.close()
        self.get_consulted()
        return formattedData

    def get_consulted(self):

        con = sqlx.connect(host = 'localhost', user = 'root', password = 'root', database = 'medicine')
        query = f'SELECT DoctorID, Username FROM DoctorUsers WHERE PATIENTS LIKE "%{self.ID}%";'
        cursor = con.cursor()
        cursor.execute(query)

        res = {}

        for doctorID, username in cursor.fetchall():

            res[doctorID] = username

        print(self.consulted)
        self.consulted = res
