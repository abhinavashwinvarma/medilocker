import mysql.connector as sqlx

user = None
userType = None

medicines = []

con = sqlx.connect(host = 'localhost', user = 'root', password = 'root', database = 'medicine')
query = f'SELECT DoctorID, Username, Qualification, Address FROM DoctorDetails;'
cursor = con.cursor()
cursor.execute(query)
doctors = cursor.fetchall()

con.close()


