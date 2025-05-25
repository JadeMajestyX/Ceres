import mysql.connector

class Database:
    def __init__(self):
        self.config = {
            'host': 'localhost',
            'user': 'root',
            'port': 3306,
            'password': '',
            'database': 'Ceres'
        }

    def connect(self):
        return mysql.connector.connect(**self.config)
