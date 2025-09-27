import  random

class Doctor:
    def __init__(self,doctorID,name):
        self.name = name
        self.doctorID = doctorID

    class Prescription:

        def __init__(self,docName, patient,medicines, clinic):
            self.docName = docName
            self.patient= patient
            #self.date= generate current time
            self.medicines=[]
            self.clinic = clinic
            #self.address = fetch address of clinic from sql db
        def add_med(self):
            name=input("Enter name of medicine: ")
            dosage= input("Enter dosage: ")
            frequency=input("Enter frequency: ")
            duration=input("Enter duration of course: ")
            notes=input("Enter any additional notes: ")
            self.medicines.append([name, dosage, frequency, duration, notes])

        def generatePrescription(doctor, clinic):

            file = open('<insertgeneratedfilename>.txt', 'w')
            l1= doctor.ljust(20) + clinic
            
            
        

'''

    def doctor_signup(self):

        username = input('Enter your username: ')
        password = input('Enter your password: ')

        self.username = username
        self.password = password
        self.doctorID = 'D' + username[:2] + str(random.randint(100000, 1000000000))

        con = sqlx.connect(host = 'localhost', user = 'root', password = 'root', database = 'Medicine')
        mycursor = con.cursor()

        query = f"INSERT INTO DoctorUsers VALUES ('{self.username}', '{self.password}', '{self.doctorID}');"

        mycursor.execute(query)
        con.commit()
        con.close()

        print(query)'''

        #def schedule_follow
