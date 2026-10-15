from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from getpass import getpass
from user import User

class ClientHelper:
    ph = PasswordHasher()

    # Validate username and password when users sign in
    # returns a User if entries are valid
    @staticmethod
    def verify_user(clients):
        
        username = input("Enter Username: ")        
        entered_password = getpass("Enter Password: ")

        # Getting the password_hash from the database if the user exists
        user_info = clients.get_username_and_password_hash(username)
        if user_info is not None:
            password_hash = user_info[0]

            # using passwordhasher to verify the hash against the entry 
            # Returns a simple user object if the password matches the hash
            try:
                ClientHelper.ph.verify(password_hash, entered_password)
                print("Password correct")
                entered_password = ""
                return User(username)
            except VerifyMismatchError:
                return 
        else:
            return 

    # Creates a user to access the program
    # returns true if the user was able to be created
    @staticmethod
    def create_user(clients):
        new_username = input("Enter Username: ")

        # Check to see if the username exists in the database
        if clients.username_exists(new_username):
            print("Username is not available.")
            return False
        
        new_password = getpass("Create Password (must be > 6 characters): ")

        # Validate the password length
        if len(new_password) < 6:
            print("Password must be at least 6 characters long")
            return False

        verify_new_password = getpass("Verify Password: ")

        # Verify that the passwords match
        if new_password != verify_new_password:
            print("Passwords don't match.")
            return False
        
        print("Passwords Match.")

        # Create the password hash to store in the database
        password_hash = ClientHelper.ph.hash(new_password)
        clients.add_user(new_username,password_hash)
        if clients.username_exists(new_username):
            print("User was created.")
            return True
        else:
            print("User was not created.")
        return False

    # Update the clients service 
    # Return True if the client was able to be updated
    @staticmethod
    def update_client(clients):
        print("   Change Client Service  ")
        print("**************************")

        # Get the user input
        client_id = input("Enter the clients ID: ")
        client_choice = input("Enter the new service ID: ")

        # Update the client 
        try:
            clients.update_client_service(client_id,client_choice)
            return True
        except ValueError as e:
            print(f"Error while updating client: {e}")
            return False

    # Add a client to the database
    # Returns true if the client was added 
    @staticmethod
    def add_client(clients):
        print("   Add a Client   ")
        print("******************")

        # Get the user input
        client_first = input("Enter first Name: ")
        client_last = input("Enter last Name: ")
        client_phone = input("Enter Phone: ")

        # Add the client
        try:
            updated_rows = clients.add_client((client_first,client_last,client_phone))
            if updated_rows:
                return True
            else:
                return False
        except ValueError as e:
            print(f"Error while updating client: {e}")
            return False

    # Remove a client using client ID
    # Returns true if the client was removed
    @staticmethod
    def remove_client(clients):
        print("   Remove a Client Record  ")
        print("***************************")

        # Get the input from the user
        client_id = input("Enter the clients ID: ")

        # Remove the client
        try:
            updated_rows = clients.remove_client_by_id(client_id)
            if updated_rows:
                return True 
            else:
                return False
        except ValueError as e:
            print(f"Error while updating client: {e}")
            return False

    # User logs in or signs up to the application
    def login_menu(clients):
        print("".ljust(50,"-"))
        print(" Hello! Welcome to our Investment Company")
        print("".ljust(50,"-"))

        # Keep displaying the menu until the user exits
        while True:
            print(" 1) Login")
            print(" 2) Signup")
            print(" 3) Quit")

            selection = input("Select an option above: ")

            # Determine the users selection 
            match selection:
                case "1":
                    user = ClientHelper.verify_user(clients)
                    if user is not None:
                        print(f"You are logged in as : {user.username}")
                        return user
                    else:
                        print(f"Username or password is incorrect")
                
                # Creating a user                        
                case "2":
                    ClientHelper.create_user(clients)   
                
                # Exits
                case "3":
                    print("Goodbye")
                    break
                case _:
                    print("Invalid choice")

    # Display the program menu
    def client_option_menu(clients):
        # Keep displaying the menu until the user exits
        while True:
            print("".ljust(50,"-"))
            print("|    Client Option Menu")
            print("|".ljust(50,"-"))
            print("| 1) Display client list")
            print("| 2) Update a clients service choice")
            print("| 3) Add a client")
            print("| 4) Remove a client")
            print("| 0) Exit")
            print("".ljust(50,"-"))
            selection = input("Pick an option  ")

            # Process the user selection 
            match selection:
                case "1":
                    print("Client List:")
                    clients.print_clean(clients.get_all_clients())
                case "2":
                    if ClientHelper.update_client(clients):
                        print("Client Updated")
                    else:
                        print("Client was not Updated")
                case "3":
                    if ClientHelper.add_client(clients):
                        print("Client Added")
                    else:
                        print("Client was not Added")
                case "4":
                    if ClientHelper.remove_client(clients):
                        print("Client Removed")
                    else:
                        print("Client was not Removed")
                case "0":
                    print("Goodbye")
                    break
                case _:
                    print("Invalid choice")