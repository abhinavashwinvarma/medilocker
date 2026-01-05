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
        self.bioDirectory = 'UserBioDataFiles/PatientBioData/'+ self.ID
        self.consulted = {}

        os.mkdir(self.fileDirectory)
        os.mkdir(self.bioDirectory)

        con = sqlx.connect(host = 'localhost', user = 'root', password = 'root', database = 'Medicine')
        mycursor = con.cursor()

        query = f"INSERT INTO PatientUsers VALUES ('{self.username}', '{self.password}', '{self.ID}', '{self.consulted}');"

        mycursor.execute(query)
        con.commit()
        con.close()
        
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
                    self.bioDirectory = 'UserBioDataFiles/PatientBioData/'+ self.ID
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

    def schedule_appointment(self, doctorID, date, time, complaint):

        con = sqlx.connect(host = 'localhost', user = 'root', password = 'root', database = 'medicine')
        query = f'INSERT INTO Appointments VALUES ("{doctorID}", "{self.ID}", "{date}", "{time}", 0, "{complaint}");'
        print(query)
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
            appointmentStatus = int(thing[-2])
            complaint = thing[-1]

            if appointmentStatus == 0:
                appointmentStatus = 'Pending request'

            elif appointmentStatus == -1:
                appointmentStatus = 'Request declined'

            else:
                appointmentStatus = 'Confirmed'

            formattedData.append([docName, appointmentDate, appointmentTime, appointmentStatus, complaint])

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

            res[doctorID] = 'Dr. ' + username

        #print(self.consulted)
        self.consulted = res

    def get_id_from_name(self, name):

        for docID in self.consulted:

            if self.consulted[docID] == name:

                return docID
    
    def update_details(self, email, phoneNum, address, dob, age = 0):

        if age == 0:

            today = datetime.date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

        delquery = f"DELETE FROM PatientDetails WHERE DoctorID = '{self.ID}'"
        record = str((self.ID, self.username, email, phoneNum, address, age, dob))
        query = f'INSERT INTO PatientDetails VALUES {record};'
        con = sqlx.connect(host = 'localhost', user = 'root', password = 'root', database = 'medicine')
        cursor = con.cursor()
        cursor.execute(delquery)
        con.commit()
        cursor.execute(query)
        con.commit()
        con.close()

    def delete_appointments(self):

        query = f'DELETE FROM Appointments WHERE STAT = -1;'
        con = sqlx.connect(host = 'localhost', user = 'root', password = 'root', database = 'medicine')
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()
        con.close()
        print(query)

    def fetch_doctors(self):

        con = sqlx.connect(host = 'localhost', user = 'root', password = 'root', database = 'medicine')
        query = "SELECT DoctorID, Username, Qualifications, Address FROM DoctorUsers NATURAL JOIN DoctorDetails;"
        cursor = con.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    
    def add_doctor(self, doctorID):

        con = sqlx.connect(host = 'localhost', user = 'root', password = 'root', database = 'medicine')
        cursor = con.cursor()
        nameQuery = f'SELECT Username FROM Doctorusers WHERE DoctorID = "{doctorID}";'
        cursor.execute(nameQuery)
        docName = cursor.fetchone()[0]

        self.consulted[doctorID] = docName
        updateQuery = f'UPDATE PatientUsers SET Doctors = "{self.consulted}" WHERE PatientID = "{self.ID}"'
        cursor.execute(updateQuery)

        fetchQuery = f'SELECT Patients FROM DoctorUsers WHERE DoctorID = "{doctorID}"'
        cursor.execute(fetchQuery)
        doctorConsulted = eval(cursor.fetchone()[0])
        doctorConsulted[self.ID] = self.username
        
        updateQuery = f'UPDATE DoctorUsers SET Patients = "{doctorConsulted}" WHERE DoctorID = "{doctorID}"'
        cursor.execute(updateQuery)
        
        con.commit()
        con.close()

    def get_account_details(self):

        con = sqlx.connect(host = 'localhost', username = 'root', password = 'root', database = 'medicine')
        cursor = con.cursor()
        query = f"SELECT Username FROM patientUsers WHERE PatientID = '{self.ID}';"
        cursor.execute(query)
        username = cursor.fetchone()[0]
        query = f"SELECT Email, Phone, DOB, Address, Conditions from PatientDetails WHERE PatientID = '{self.ID}';"
        cursor.execute(query)
        accountDetails = cursor.fetchone()
        accountDetails = (username, ) + accountDetails
        return accountDetails