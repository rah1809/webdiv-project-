from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Database:
    def __init__(self):
        # Create a MongoDB client
        self.client = MongoClient('mongodb://localhost:27017/')
        # Connect to the ResearchDB database
        self.db = self.client['ResearchDB']
        # Get collections
        self.login_collection = self.db['Login']
        self.user_profiles = self.db['UserProfiles']


    def add_user(self, username, password):
        """Add a new user to the database"""
        # Check if username already exists
        if self.login_collection.find_one({'username': username}):
            return False, "Username already exists"
        
        # Create new user document
        user = {
            'username': username,
            'password': generate_password_hash(password),
            'created_at': datetime.utcnow(),
            'last_login': None,
            'is_active': True
        }
        
        # Insert the user login credentials
        self.login_collection.insert_one(user)
        
        # Create user profile
        user_profile = {
            'username': username,
            'email': email,
            'full_name': full_name,
            'registration_date': datetime.utcnow(),
            'profile_completed': False,
            'research_interests': [],
            'university': None,
            'department': None,
            'student_id': None,
            'projects': [],
            'publications': []
        }
        
        # Insert the user profile
        self.user_profiles.insert_one(user_profile)
        return True, "Registration successful"

    def verify_user(self, username, password):
        """Verify user credentials and update last login"""
        user = self.login_collection.find_one({'username': username})
        
        if user and check_password_hash(user['password'], password):
            # Update last login time
            self.login_collection.update_one(
                {'username': username},
                {'$set': {'last_login': datetime.utcnow()}}
            )
            return True
        return False

    def get_user_profile(self, username):
        """Retrieve user profile information"""
        return self.user_profiles.find_one({'username': username})

    def update_user_profile(self, username, profile_data):
        """Update user profile information"""
        result = self.user_profiles.update_one(
            {'username': username},
            {'$set': profile_data}
        )
        return result.modified_count > 0

    def delete_user(self, username):
        """Delete user and associated profile"""
        # Delete from login collection
        self.login_collection.delete_one({'username': username})
        # Delete from profiles collection
        self.user_profiles.delete_one({'username': username})
        return True

    def change_password(self, username, old_password, new_password):
        """Change user password"""
        if self.verify_user(username, old_password):
            self.login_collection.update_one(
                {'username': username},
                {'$set': {'password': generate_password_hash(new_password)}}
            )
            return True
        return False

    def deactivate_user(self, username):
        """Deactivate user account"""
        result = self.login_collection.update_one(
            {'username': username},
            {'$set': {'is_active': False}}
        )
        return result.modified_count > 0

    def reactivate_user(self, username):
        """Reactivate user account"""
        result = self.login_collection.update_one(
            {'username': username},
            {'$set': {'is_active': True}}
        )
        return result.modified_count > 0

    def user_exists(self, username):
        """Check if username exists"""
        return self.login_collection.find_one({'username': username}) is not None
