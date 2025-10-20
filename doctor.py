import prescriptionGenerator
import mysql.connector as sqlx
import os 
import random

class Doctor:

    def __init__(self):

        self.logged_in = False

    def signup(self, username: str, password: str):
        
        self.username: str = username
        self.password: str = password
        self.doctorID: str = 'Dr' + username[:2] + str(random.randint(100000, 999999)) #format: DrAB240095
        self.doc_file_directory: str = 'DoctorFiles/'+ self.doctorID
        os.mkdir(self.doc_file_directory)

        con = sqlx.connect(host = 'localhost', user = 'root', password = 'root', database = 'Medicine')
        mycursor = con.cursor()

        query = f"INSERT INTO DoctorUsers VALUES ('{self.username}', '{self.password}', '{self.doctorID}');"

        mycursor.execute(query)
        con.commit()
        con.close()

        print('Sign-up success!')

        self.logged_in = True

    def login(self, username, password):

        con = sqlx.connect(host = 'localhost', user = 'root', password = 'root', database = 'Medicine')
        mycursor = con.cursor()
        mycursor.execute('SELECT * FROM DoctorUsers;')
        
        for record in mycursor.fetchall():

            print(record)
            if username in record:
                correct_password = record[1]

                if password == correct_password:
                    print('Login success!')
                    self.logged_in = True
                    self.username = username
                    self.password = correct_password
                    self.doctorID = record[-1]
                    break

                else:
                    print('Incorrect password.')
                    break
            
        if not self.logged_in:
            
            print('This user does not exist.') 

    def finish_appointment(self, patientID, diagnosis):

        con = sqlx.connect(host = '127.0.0.1',user = 'root', password = 'root', database = 'medicine')
        cur = con.cursor()
        queryName = f"SELECT USERNAME FROM patientUsers WHERE Patient_ID = '{patientID}'"
        queryAge = f"SELECT AGE FROM patientdetails WHERE Patient_ID = '{patientID}'"
        medicines = [['Nimbadi', 'light dose','Frequency 1', 'Duration 1', 'Notes'],['medicine 2', 'heavy dose', 'very frequent', 'long duration', 'notessssssssssssssssssssssssss' ]]
        cur.execute(queryName)
        patientName = cur.fetchall()[0][0]
        cur.execute(queryAge)
        patientAge = cur.fetchall()[0][0]
        prescriptionGenerator.create_prescription(self.doctorID, self.docName, self.qualifications, patientName, patientAge, diagnosis, medicines, self.clinicName, self.clinicAddress, self.clinicLogoPath, self.signature)
    
    def logout(self):

        self.logged_in = False
        self.username = ''
        self.password = ''
        self.doctorID = ''





            
            


