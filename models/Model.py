import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.Database import Database

class Model:
    def __init__(self):
        self.db = Database()
        self.connection = self.db.connect()
        self.cursor = self.connection.cursor(dictionary=False)

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
