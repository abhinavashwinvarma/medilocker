import random
import os

class Patient:

    def __init__(self, patientID):

        self.patientID = patientID
        self.saved_files = os.listdir('PatientFiles/' + self.patientID)
        self.saved_files = ['PatientFiles/' + self.patientID + '/' + file for file in self.saved_files]        
    
    def view_file(self, file_name):

        filepath = ''
        for item in self.saved_files:

            if file_name in item:
                filepath = item
                break

    

        