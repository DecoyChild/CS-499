import mysql.connector
from mysql.connector import Error

## Class to manage the databse connection
class DatabaseHelper:

    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            # Credentials for the database and returns the connection
            self.connection = mysql.connector.connect(
                host='localhost',          
                database='client_manager', 
                user='decoy',              
                password='#%36HivL'   
            )
            return self.connection
                
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            raise

    # Close the connection if one is open
    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

    # Returning the database connection. 
    # reconnecting if the connection was lost
    def get_connection(self):
        if not self.connection or not self.connection.is_connected():
            self.connect()
        return self.connection
    
