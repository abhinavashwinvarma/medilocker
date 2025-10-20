import random
import os
import mysql.connector as sqlx


class Patient:

    def __init__(self):

        self.logged_in = False
          
    def signup(self, username: str, password: str):
        
        self.username: str = username
        self.password: str = password
        self.patientID: str = username[:2] + str(random.randint(100000, 1000000000))
        self.patient_file_directory: str = 'PatientFiles/'+ self.patientID
        os.mkdir(self.patient_file_directory)

        con = sqlx.connect(host = 'localhost', user = 'root', password = 'root', database = 'Medicine')
        mycursor = con.cursor()

        query = f"INSERT INTO PatientUsers VALUES ('{self.username}', '{self.password}', '{self.patientID}');"

        mycursor.execute(query)
        con.commit()
        con.close()

        #print(query)
        print('Sign-up success!')

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
                    self.patientID = record[-1]
                    self.patient_file_directory: str = 'PatientFiles/'+ self.patientID

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
        self.patientID = ''

    def access_files(self):

        for file in os.listdir(self.patient_file_directory):

            print(file)

    def schedule_appointment(self, doctorID, date, time):

        con = sqlx.connect(host = 'localhost', user = 'root', password = 'root', database = 'medicine')
        query = f'INSERT INTO Appointments VALUES ("{doctorID}", "{self.patientID}", "{date}", "{time}");'
        #print(query)
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()
        con.close()

    