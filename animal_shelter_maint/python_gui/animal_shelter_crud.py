# Example Python Code to Insert a Document 

from pymongo import MongoClient 
from bson.objectid import ObjectId 
from urllib.parse import quote_plus

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 
    # default to blank for error catch
    # Updated to take database info as parameters for portability
    def __init__(self, USER='', PASS='',HOST='localhost', PORT = 27017,DB = 'aac',COL = 'animals'): 
        # Initializing the MongoClient. This helps to access the MongoDB 
        # Initialize Connection 
        try:
            self.client = MongoClient('mongodb://%s:%s@%s:%d' % (quote_plus(USER),quote_plus(PASS),HOST,PORT)) 
            self.database = self.client['%s' % (DB)] 
            self.collection = self.database['%s' % (COL)] 
        except Exception as e:
            print(f'There was an error establishing a connection to the database: \n\t{e}')

    # Creating a document from a valid dictionary 
    # Returns True for a successful insert, False for a failure
    def create(self, data = None):
        if data is not None: 
            # exception is printed to the screen if an error occors
            try:
                self.database.animals.insert_one(data)  # data should be dictionary             
                return True
            except Exception as e:
                print(f'There was an error creating a new record:\n\t-{e}')
                return False
        else: 
            raise Exception("Nothing to save, because data parameter is empty") 

            
    # find the docuemnt(s) in the database and return as a list. 
    # An empty list will be return if nothing is found
    def read(self, find_set = None):
        
        try:
            # using the search set, point the cursor at the first element found
            doc_cursor = self.database.animals.find(find_set)            
        except Exception as e:
            # Print any exceptions and return an empty list
            print(f'There was an error in the read function:\n\t-{e}')
            return []
        else:
            # list to return the results 
            document_list = [] 
            
            # Iterate through the cursor as long as it hasNext and append the document list
            for document in doc_cursor:
                document_list.append(document)            
            return document_list
    
    # Update an existing record
    def update(self,find_set = None, update_set = None):
        if find_set is None or update_set is None:
            print('Must Criteria to update a Document.')
            return 0
        
        # Setting up the update values parameters 
        update_values = { "$set":update_set }
        try:
            update_results = self.database.animals.update_many(find_set,update_values)
        except Exception as e:
            print(f'There was an error trying to update a document: {e}')
            return 0
        else:
            return update_results.modified_count
                
    # delete a specified set of documents based on key value pair
    # NOTE to safeguard against deleting an entire collection, a blank set will not be accepted 
    def delete(self,find_set = None):
        # don't delete all docuemts in the collection 
        if not find_set:
            print('Please send at least one filter to delete.')
            return 0
        else:
            try:
                # delete all documents that match given criteria
                delete_results = self.database.animals.delete_many(find_set)
            except Exception as e:
                print(f'There was an error deleting documents:{e}')
                return 0
            else:
                # get the number of documents that were deleted 
                return delete_results.deleted_count
        
        
    
    
        