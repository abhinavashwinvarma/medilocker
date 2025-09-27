import mysql.connector as sqlx
import random
import os
import pickle

class App:

    def __init__(self):

        self.logged_in: bool = False

    def patient_signup(self):

        username = input('Enter your username: ')
        password = input('Enter your password: ')

        self.username: str = username
        self.password: str = password
        self.patientID: str = username[:2] + str(random.randint(100000, 1000000000))

        os.mkdir('PatientFiles/'+ self.__doc__patientID)

        con = sqlx.connect(host = 'localhost', user = 'root', password = 'root', database = 'Medicine')
        mycursor = con.cursor()

        query = f"INSERT INTO PatientUsers VALUES ('{self.username}', '{self.password}', '{self.patientID}');"

        mycursor.execute(query)
        con.commit()
        con.close()

        print(query)
        print('Sign-up success!')

        self.logged_in = True


    def patient_login(self):

        username = input('Enter your username: ')

        con = sqlx.connect(host = 'localhost', user = 'root', password = 'root', database = 'Medicine')
        mycursor = con.cursor()
        mycursor.execute('SELECT * FROM PatientUsers;')
        
        for record in mycursor.fetchall():

            if username in record:
                
                correct_password = record[1]
                password = input('Welcome back! Enter your password: ')

                if password == correct_password:

                    print('Login success!')
                    self.logged_in = True
                    self.username = username
                    self.password = correct_password
                    self.patientID = record[-1]
                    break

                else:

                    print('Incorrect password.')
                    break
            
            else:

                print('This user does not exist.')
                break

        con.close()

    def patient_logout(self):

        self.logged_in = False
        self.username = ''
        self.password = ''
        self.patientID = ''

    
    