from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
    """ CRUD Operations for Animal Collection in MongoDB """
    
    # Declare one's self into existence
    def __init__(self, username, password):
        self.client = MongoClient('mongodb://%s:%s@localhost:48219/?authMechanism=DEFAULT&authSource=admin'%(username, password))
        self.database = self.client['AAC']
    
    # Insert data into the animals collection
    def create(self, data):
        
        # Double-check the user actually provided data to be created
        if data is None:
            raise Exception("PLEASE NOTE: Data must be provided in order to be saved.")
        
        # Instantiate a variable for the created data to utilize as an "existence check"
        saved = self.database.animals.insert_one(data)
        
        # Subsequently, check if the created data is null within the animals collection
        # Return False or True depending on the result
        return False if saved is None else True
    
    # Search for data within the animals collection
    def read(self, query):
        
        # Double-check the user actually provided a query to be filtered with
        if query is None:
            raise Exception("PLEASE NOTE: Cannot search for something that is not requested.")
        
        # Return the data that results from the query search
        return self.database.animals.find_one(query)
    
    # Pull all data within the animals collection
    def readAll(self, data):
        
        # Return a cursor that acts like a stopping point of all data before it
        cursor = self.database.animals.find(data, {"_id":False})
        return cursor
    
    # Update data that is already present in the animals collection
    def update(self, query, data):
        
        # Double-check the user actually provided data to be updated
        if data is None:
            raise Exception("PLEASE NOTE: In order to update, new information must be provided.")
        
        # Double-check the user wishes to update information that can be updated instead of created
        if query is None:
            raise Exception("PLEASE NOTE: In order to update, present information must be provided.\nOtherwise, create data instead.")
        
        # Updating is involved.  TRY to see if it is successful
        try:
            updated = self.database.animals.find_one_and_update(query, {"$set":data}, {"upsert":True, "new":True})
            
            # Check if the update was successful or not based on if the newly updated document was returned...
            if updated is not None:
                
                # ... if so, return the data as a JSON
                print("PLEASE NOTE: Successful update.")
                return updated
            else:
                
                # ... and if not, let the user know
                raise Exception("ERROR: Could not update the query.")
                
        except Exception as exc:
            print("ERROR: Something went wrong in the updating process:", exc)
    
    # Delete data from the animals collection
    def delete(self, data):
        
        # Double-check the user actually provided data to be deleted
        if data is None:
            raise Exception("PLEASE NOTE: To delete one's self, one's self must present one's self to be deleted.")
        
        # Deleting is involved; TRY it to see if it is successful
        try:
            preDeleted = self.database.animals.find_one(data)
            deleted = self.database.animals.find_one_and_delete(data, {"new":False})
            
            # Check if the deletion registers...
            if deleted is not None:
                
                # ... if so, let the user know and return the deleted data as affirmation...
                print("PLEASE NOTE: Deletion successful.")
                return preDeleted
            else:
                
                # ... otherwise, let the user know deletion did not occur
                raise Exception("PLEASE NOTE: Nothing could be deleted with the given parameters.")
        
        # If the deletion attempt was unsuccessful for any reason, showcase the error to the user
        except Exception as exc:
            print("ERROR: Something went wrong in the deletion process:", exc)