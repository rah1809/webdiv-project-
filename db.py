from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from bson.objectid import ObjectId

class Database:
    def __init__(self):
        try:
            # Create a MongoDB client
            self.client = MongoClient('mongodb://localhost:27017/')
            
            # Connect to the ResearchDB database
            self.db = self.client['ResearchDB']
            
            # Initialize collections
            self.login_collection = self.db['Login']
            self.user_profiles = self.db['UserProfiles']
            self.data_analysis = self.db['DataAnalysis']
            self.research_groups = self.db['ResearchGroups']
            self.online_users = self.db['OnlineUsers']
            
            # Test connection
            self.client.admin.command('ping')
            print(f"Successfully connected to MongoDB. Database: {self.db.name}")
            
            # Create indexes
            self._create_indexes()
            
        except Exception as e:
            print(f"Database connection error: {e}")
            raise

    def _create_indexes(self):
        """Create necessary indexes for better performance"""
        try:
            # Unique indexes
            self.collections['login'].create_index('username', unique=True)
            self.collections['profiles'].create_index('username', unique=True)
            self.collections['online_users'].create_index('username', unique=True)
            
            # Regular indexes for frequent queries
            self.collections['analyses'].create_index([('username', 1), ('created_at', -1)])
            self.collections['groups'].create_index('members')
            self.collections['projects'].create_index('participants')
            
        except Exception as e:
            print(f"Error creating indexes: {e}")

    def test_connection(self):
        """Test database connection"""
        try:
            # Ping the database
            self.client.admin.command('ping')
            print("✅ Successfully connected to MongoDB!")
            
            # Print database information
            print("\nDatabase Information:")
            print(f"Database name: {self.db_name}")
            print("\nCollections:")
            for collection in self.db.list_collection_names():
                count = self.db[collection].count_documents({})
                print(f"- {collection} (Documents: {count})")
            
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False


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

    def get_online_users(self):
        """Get list of currently online users"""
        try:
            online_users = list(self.db['OnlineUsers'].find({}, {'username': 1, '_id': 0}))
            return [user['username'] for user in online_users]
        except:
            return []

    def add_analysis(self, username, title, description, data_type, results=None):
        """Add a new data analysis entry"""
        analysis = {
            'username': username,
            'title': title,
            'description': description,
            'data_type': data_type,
            'results': results,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'status': 'pending'
        }
        
        result = self.db['DataAnalysis'].insert_one(analysis)
        return str(result.inserted_id)

    def get_user_analyses(self, username):
        """Get all analyses for a user"""
        return list(self.db['DataAnalysis'].find({'username': username}))

    def update_analysis(self, analysis_id, update_data):
        """Update an analysis entry"""
        update_data['updated_at'] = datetime.utcnow()
        result = self.db['DataAnalysis'].update_one(
            {'_id': ObjectId(analysis_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0

    def delete_analysis(self, analysis_id, username):
        """Delete an analysis entry"""
        result = self.db['DataAnalysis'].delete_one({
            '_id': ObjectId(analysis_id),
            'username': username  # Ensure user owns the analysis
        })
        return result.deleted_count > 0

    def get_user_data(self, username):
        """Get user information from database"""
        query = "SELECT username, email, full_name, created_at FROM users WHERE username = ?"
        result = self.execute_query(query, (username,), fetch_one=True)
        return result if result else None

    def get_recent_activities(self, username):
        """Get user's recent activities"""
        query = """
            SELECT activity_type, description, created_at 
            FROM user_activities 
            WHERE username = ? 
            ORDER BY created_at DESC 
            LIMIT 10
        """
        return self.execute_query(query, (username,), fetch_all=True)

    def update_last_login(self, username):
        """Update user's last login timestamp"""
        query = "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE username = ?"
        self.execute_query(query, (username,))
        self.conn.commit()

    def get_analysis_by_id(self, analysis_id):
        """Get analysis by ID"""
        try:
            return self.db['DataAnalysis'].find_one({'_id': ObjectId(analysis_id)})
        except:
            return None

    def get_user_collaborators(self, username):
        """Get user's collaborators from research groups"""
        collaborators = set()
        groups = self.db['ResearchGroups'].find({'members': username})
        
        for group in groups:
            collaborators.update(group['members'])
        
        collaborators.discard(username)  # Remove self from list
        return list(collaborators)

    def share_analysis(self, analysis_id, shared_with):
        """Share analysis with other users"""
        result = self.db['DataAnalysis'].update_one(
            {'_id': ObjectId(analysis_id)},
            {'$addToSet': {'shared_with': {'$each': shared_with}}}
        )
        return result.modified_count > 0

    def prepare_analysis_export(self, analysis_id):
        """Prepare analysis data for export"""
        analysis = self.get_analysis_by_id(analysis_id)
        if not analysis:
            return None
            
        return {
            'title': analysis['title'],
            'description': analysis['description'],
            'data_type': analysis['data_type'],
            'results': analysis['results'],
            'created_at': analysis['created_at'].isoformat(),
            'status': analysis['status']
        }

    def get_related_analyses(self, analysis_id):
        """Get related analyses based on data type and content"""
        analysis = self.get_analysis_by_id(analysis_id)
        if not analysis:
            return []
            
        return list(self.db['DataAnalysis'].find({
            '_id': {'$ne': ObjectId(analysis_id)},
            'data_type': analysis['data_type']
        }).limit(5))
