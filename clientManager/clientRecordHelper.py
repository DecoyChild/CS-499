# Using paramarized queries 
class ClientRecordHelper:
    
    def __init__(self, database):
        self.db = database

    # Get all the clients from the database 
    def get_all_clients(self):
        cursor =  self.get_cursor()
        select_q = "SELECT * FROM clients"
        cursor.execute(select_q)
        return cursor.fetchall()

    # Gets all the services available 
    def get_all_services(self):
        cursor =  self.get_cursor()
        select_q = "SELECT * FROM services"
        cursor.execute(select_q)    
        return cursor.fetchall()

    # Lookup a client from the client ID
    def get_client_by_id(self, id:int):
        cursor = self.get_cursor() 
        select_q = "SELECT * FROM clients WHERE client_id = %s"
        cursor.execute(select_q, (id,))
        return cursor.fetchone()

    # Get the service description from the ID
    def get_service_desc(self, id:int):
        cursor = self.get_cursor() 
        select_q = "SELECT service_name FROM services WHERE service_id = %s"
        cursor.execute(select_q, (id,))
        return cursor.fetchone()

    # Update a clients service choice
    def update_client_service(self, id:int, service_id:int):
        cursor = self.get_cursor()
        update_q = "UPDATE clients SET service_choice = %s WHERE client_id = %s"
        cursor.execute(update_q, (service_id,id))
        return cursor.rowcount

    # Add a client 
    def add_client(self, user_data:dict):
        cursor = self.get_cursor()
        # using parameterized queries
        insert_q = "INSERT INTO clients (first_name, last_name, phone) VALUES (%s, %s, %s)"
        cursor.execute(insert_q, user_data)
        self.db.get_connection().commit()
        return cursor.rowcount

    # Add a user for the application
    def add_user(self, username:str, password_hash:str):
        cursor = self.get_cursor()
        
        # See if the username exists
        select_q = "SELECT COUNT(*) FROM users WHERE username = %s"
        cursor.execute(select_q, (username,))
        count = cursor.fetchone()

        # If there are any results don't try to add the user
        if (count[0] == 0):
            insert_q = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
            cursor.execute(insert_q, (username,password_hash))
            self.db.get_connection().commit()
            return cursor.rowcount
        else:
            return "User alrady exists"

    # Get the password hash to verify against entered password
    def get_username_and_password_hash(self, username:str):
        cursor = self.get_cursor()
        select_q = "SELECT password_hash FROM users WHERE username = %s"
        cursor.execute(select_q, (username,))
        record = cursor.fetchone()

        # returns the record 
        if record is not None:
            return record
        else:
            return

    # Returns true if the user exists
    def username_exists(self, username:str):
        cursor = self.get_cursor()
        select_q = "SELECT COUNT(*) FROM users WHERE username = %s"
        cursor.execute(select_q, (username,))
        record = cursor.fetchone()
        if record[0] > 0:
            return True
        else:
            return False

    # Removes a client 
    def remove_client_by_id(self, id:int):
        cursor = self.get_cursor()
        delete_q = "DELETE FROM clients where client_id = %s"
        cursor.execute(delete_q, (id,))
        self.db.get_connection().commit()
        return cursor.rowcount

    # Gets a cursor
    def get_cursor(self):
            connection = self.db.get_connection()
            return connection.cursor()

    # Prints the clients in a clean format
    def print_clean(self, record:list):
        
        for elem in record:
            service_name = self.get_service_desc(elem[4])[0]
            print("".ljust(50,"*"))
            print(f"Client ID: {elem[0]}")
            print(f"Name: {elem[1]} {elem[2]}")
            print(f"Phone: {elem[3]}")
            print(f"Service Choice: {elem[4]} : {service_name}")
            
        
    