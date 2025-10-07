import mysql.connector as sqlx
import random
import os
import pickle

class App:

    def __init__(self):

        self.logged_in: bool = False

    