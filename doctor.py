import prescriptionGenerator
import mysql.connector as sqlx
import os 
import random

class Doctor:

    def __init__(self):

        self.logged_in = False
        self.qualifications = 'MBBS'

    def signup(self, username: str, password: str):
        
        self.username: str = username
        self.password: str = password
        self.ID: str = 'Dr' + username[:2] + str(random.randint(100000, 999999)) #format: DrAB240095
        self.fileDirectory: str = 'DoctorFiles/'+ self.ID
        self.bioDirectory = 'UserBioDataFiles/DoctorBioData/'+ self.ID
        self.consulted = {}
        os.mkdir(self.fileDirectory)
        os.mkdir(self.bioDirectory)

        con = sqlx.connect(host = 'localhost', user = 'root', password = 'root', database = 'Medicine')
        mycursor = con.cursor()

        query = f"INSERT INTO DoctorUsers VALUES ('{self.username}', '{self.password}', '{self.ID}', '{self.consulted}');"

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

            if username in record:
                correct_password = record[1]

                if password == correct_password:
                    #print('Login success!')
                    self.logged_in = True
                    self.username = username
                    self.password = correct_password
                    self.ID = record[-2]
                    self.consulted = eval(record[-1])
                    self.bioDirectory = 'UserBioDataFiles/DoctorBioData/'+ self.ID
                    self.fileDirectory = 'DoctorFiles/'+ self.ID

                    query = f'SELECT Address, Qualification from DoctorDetails where DoctorID = "{self.ID}";'
                    mycursor.execute(query)

                    record = mycursor.fetchone()
                    self.address = record[0]
                    self.qualifications = record[1]

                    #print(self.consulted)
                    break

                else:
                    #print('Incorrect password.')
                    break
            
        #if not self.logged_in:
            
            #print('This user does not exist.') 

    def get_appointments(self):

        con = sqlx.connect(host = 'localhost', user = 'root', password = 'root', database = 'medicine')
        query = f'SELECT * FROM Appointments WHERE DoctorID = "{self.ID}";'
        cursor = con.cursor()
        cursor.execute(query)
        
        data = cursor.fetchall()
        formattedData = []
        
        for thing in data:

            cursor.execute(f'SELECT Username FROM PatientUsers WHERE PatientID = "{thing[1]}"')
            patientName = 'Mr. ' + cursor.fetchone()[0]
            appointmentDate = thing[2]
            appointmentTime = thing[3]
            appointmentStatus = (int(thing[-2]))
            complaint = thing[-1]

            if appointmentStatus == 0:
                appointmentStatus = 'Pending request'

            elif appointmentStatus == -1:
                appointmentStatus = 'Request declined'

            else:
                appointmentStatus = 'Confirmed'

            formattedData.append([patientName, appointmentDate, appointmentTime, appointmentStatus, complaint])

        con.close()
        self.get_consulted()
        return formattedData

    def get_consulted(self):

        con = sqlx.connect(host = 'localhost', user = 'root', password = 'root', database = 'medicine')
        query = f'SELECT PatientID, Username FROM PatientUsers WHERE DOCTORS LIKE "%{self.ID}%";'
        cursor = con.cursor()
        cursor.execute(query)
        res = {}

        for patientID, username in cursor.fetchall():

            res[patientID] = username

        #print(self.consulted)
        self.consulted = res
        con.close()

    def get_id_from_name(self, name):

        for patientID in self.consulted:

            if self.consulted[patientID] == name:

                return patientID

    def accept_appointment(self, record):

        query = f'UPDATE Appointments SET Stat = 1 WHERE DoctorID = "{self.ID}" AND AppointmentDate = "{record[1]}" AND AppointmentTime = "{record[2]}";'
        con = sqlx.connect(host = 'localhost', user = 'root', password = 'root', database = 'medicine')
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()
        con.close()
        
    def reject_appointment(self, record):

        query = f'UPDATE Appointments SET Stat = -1 WHERE DoctorID = "{self.ID}" AND AppointmentDate = "{record[1]}" AND AppointmentTime = "{record[2]}"'
        con = sqlx.connect(host = 'localhost', user = 'root', password = 'root', database = 'medicine')
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()
        con.close()

    def finish_appointment(self, record):

        query = f'DELETE FROM Appointments WHERE DoctorID = "{self.ID}" AND AppointmentDate = "{record[1]}" AND AppointmentTime = "{record[2]}"'
        con = sqlx.connect(host = 'localhost', user = 'root', password = 'root', database = 'medicine')
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()
        con.close()

    def share_prescription(self, patientID, diagnosis, medicines):

        con = sqlx.connect(host = '127.0.0.1',user = 'root', password = 'root', database = 'medicine')
        cur = con.cursor()

        queryName = f"SELECT USERNAME FROM PatientDetails WHERE PatientID = '{patientID}';"
        queryAge = f"SELECT AGE FROM PatientDetails WHERE PatientID = '{patientID}';"

        print(queryAge)
        print(queryName)
        cur.execute(queryName)
        patientName = cur.fetchone()[0]
        print(patientName)
        cur.execute(queryAge)
        patientAge = cur.fetchone()[0]

        self.clinicName = 'CLINIC 101'
                
        prescriptionGenerator.create_prescription(self.ID, patientID, self.username, self.qualifications, patientName, patientAge, diagnosis, medicines, self.clinicName, self.address)
        con.close()

    def update_details(self, email, phoneNum, address, qualifications, dob):

        self.address = address
        self.qualifications = qualifications

        record = str((self.ID, self.username, email, phoneNum, address, qualifications, dob))
        delquery = f'DELETE FROM DoctorDetails WHERE DoctorID = "{self.ID}";'
        query = f'INSERT INTO DoctorDetails VALUES {record};'
        con = sqlx.connect(host = 'localhost', user = 'root', password = 'root', database = 'medicine')
        cursor = con.cursor()
        cursor.execute(delquery)
        con.commit()
        cursor.execute(query)
        con.commit()
        con.close()

    def get_account_details(self):
        
        con = sqlx.connect(host = 'localhost', username = 'root', password = 'root', database = 'medicine')
        cursor = con.cursor()
        query = f"SELECT Username FROM DoctorUsers WHERE DoctorID = '{self.ID}';"
        cursor.execute(query)
        username = cursor.fetchone()[0]

        query = f"SELECT Email, Phone, DOB, Address, Qualification FROM DoctorDetails WHERE DoctorID = '{self.ID}';"
        cursor.execute(query)
        accountDetails = cursor.fetchone()
        accountDetails = (username, ) + accountDetails
        
        return accountDetails

    def logout(self):

        self.logged_in = False
        self.username = ''
        self.password = ''
        self.ID = ''





            
            


