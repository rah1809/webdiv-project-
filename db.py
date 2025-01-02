from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

class Database:
    def __init__(self):
        # Create a MongoDB client
        self.client = MongoClient('mongodb://localhost:27017/')
        # Connect to the ResearchDB database
        self.db = self.client['ResearchDB']
        # Get the Login collection
        self.login_collection = self.db['Login']

    def add_user(self, username, password):
        """Add a new user to the database"""
        # Check if username already exists
        if self.login_collection.find_one({'username': username}):
            return False
        
        # Create new user document
        user = {
            'username': username,
            'password': generate_password_hash(password)
        }
        
        # Insert the user
        self.login_collection.insert_one(user)
        return True

    def verify_user(self, username, password):
        """Verify user credentials"""
        user = self.login_collection.find_one({'username': username})
        
        if user and check_password_hash(user['password'], password):
            return True
        return False
