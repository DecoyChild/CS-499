from databaseHelper import DatabaseHelper
from clientRecordHelper import ClientRecordHelper
from user import User
from clientHelper import ClientHelper

# Establish a database connection 
db = DatabaseHelper()

# intializing a client Record object
clients = ClientRecordHelper(db)  

# Getting the user object from the login menu
user = ClientHelper.login_menu(clients)

# If a valid user is found then display the program options
if user is not None:
    ClientHelper.client_option_menu(clients)

# Cleanup - Closing the database and exit
db.close()
exit()  