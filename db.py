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
            self.library_collection = self.db['library']
            
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
            self.collections['Login'].create_index('username', unique=True)
            self.collections['Profiles'].create_index('username', unique=True)
            self.collections['Online_users'].create_index('username', unique=True)
            
            # Regular indexes for frequent queries
            self.collections['Data Analyses'].create_index([('username', 1), ('created_at', -1)])
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

    def create_research_profile(self, username, profile_data):
        """Create or update a research profile"""
        try:
            profile = {
                'username': username,
                'full_name': profile_data.get('full_name'),
                'department': profile_data.get('department'),
                'institution': profile_data.get('institution'),
                'research_interests': profile_data.get('research_interests', []),
                'education': profile_data.get('education', []),
                'publications': profile_data.get('publications', []),
                'projects': profile_data.get('projects', []),
                'contact_info': {
                    'email': profile_data.get('email'),
                    'phone': profile_data.get('phone'),
                    'office': profile_data.get('office')
                },
                'social_links': profile_data.get('social_links', {}),
                'updated_at': datetime.utcnow()
            }
            
            result = self.db['ResearchProfiles'].update_one(
                {'username': username},
                {'$set': profile},
                upsert=True
            )
            return True, "Profile updated successfully"
        except Exception as e:
            return False, str(e)

    def get_research_profile(self, username):
        """Get research profile by username"""
        try:
            profile = self.db['ResearchProfiles'].find_one({'username': username})
            return profile
        except:
            return None

    def add_publication(self, username, publication_data):
        """Add a publication to research profile"""
        publication = {
            'title': publication_data.get('title'),
            'authors': publication_data.get('authors', []),
            'journal': publication_data.get('journal'),
            'year': publication_data.get('year'),
            'doi': publication_data.get('doi'),
            'citation_count': publication_data.get('citation_count', 0),
            'added_at': datetime.utcnow()
        }
        
        result = self.db['ResearchProfiles'].update_one(
            {'username': username},
            {'$push': {'publications': publication}}
        )
        return result.modified_count > 0

    def add_research_project(self, username, project_data):
        """Add a research project"""
        project = {
            'title': project_data.get('title'),
            'description': project_data.get('description'),
            'start_date': project_data.get('start_date'),
            'end_date': project_data.get('end_date'),
            'status': project_data.get('status', 'ongoing'),
            'collaborators': project_data.get('collaborators', []),
            'funding': project_data.get('funding'),
            'added_at': datetime.utcnow()
        }
        
        result = self.db['ResearchProfiles'].update_one(
            {'username': username},
            {'$push': {'projects': project}}
        )
        return result.modified_count > 0

    def update_research_stats(self, username):
        """Update research statistics"""
        profile = self.get_research_profile(username)
        if not profile:
            return False
            
        stats = {
            'publication_count': len(profile.get('publications', [])),
            'project_count': len(profile.get('projects', [])),
            'total_citations': sum(pub.get('citation_count', 0) for pub in profile.get('publications', [])),
            'h_index': self._calculate_h_index(profile.get('publications', [])),
            'updated_at': datetime.utcnow()
        }
        
        result = self.db['ResearchProfiles'].update_one(
            {'username': username},
            {'$set': {'research_stats': stats}}
        )
        return result.modified_count > 0

    def _calculate_h_index(self, publications):
        """Calculate h-index from publications"""
        if not publications:
            return 0
            
        citations = sorted([pub.get('citation_count', 0) for pub in publications], reverse=True)
        h = 0
        for i, citations_count in enumerate(citations, 1):
            if citations_count >= i:
                h = i
            else:
                break
        return h

    def update_student_profile(self, username, profile_data):
        """Update student research profile"""
        try:
            profile = {
                'username': username,
                'student_id': profile_data.get('student_id'),
                'full_name': profile_data.get('full_name'),
                'university': profile_data.get('university'),
                'department': profile_data.get('department'),
                'degree_program': profile_data.get('degree_program'),
                'year_of_study': profile_data.get('year_of_study'),
                'research_topics': profile_data.get('research_topics', []),
                'supervisor': profile_data.get('supervisor'),
                'academic_details': {
                    'gpa': profile_data.get('gpa'),
                    'expected_graduation': profile_data.get('expected_graduation'),
                    'thesis_topic': profile_data.get('thesis_topic')
                },
                'contact_info': {
                    'email': profile_data.get('email'),
                    'phone': profile_data.get('phone'),
                    'office_location': profile_data.get('office_location')
                },
                'research_interests': profile_data.get('research_interests', []),
                'skills': profile_data.get('skills', []),
                'certifications': profile_data.get('certifications', []),
                'updated_at': datetime.utcnow()
            }
            
            result = self.db['StudentProfiles'].update_one(
                {'username': username},
                {'$set': profile},
                upsert=True
            )
            return True, "Profile updated successfully"
        except Exception as e:
            return False, str(e)

    def get_student_profile(self, username):
        """Get student profile by username"""
        try:
            return self.db['StudentProfiles'].find_one({'username': username})
        except Exception as e:
            print(f"Error retrieving student profile: {e}")
            return None

    def add_research_topic(self, username, topic_data):
        """Add a research topic to student profile"""
        topic = {
            'title': topic_data.get('title'),
            'description': topic_data.get('description'),
            'category': topic_data.get('category'),
            'status': topic_data.get('status', 'ongoing'),
            'start_date': topic_data.get('start_date'),
            'supervisor': topic_data.get('supervisor'),
            'added_at': datetime.utcnow()
        }
        
        result = self.db['StudentProfiles'].update_one(
            {'username': username},
            {'$push': {'research_topics': topic}}
        )
        return result.modified_count > 0

    def update_academic_progress(self, username, progress_data):
        """Update academic progress"""
        progress = {
            'semester': progress_data.get('semester'),
            'gpa': progress_data.get('gpa'),
            'completed_credits': progress_data.get('completed_credits'),
            'research_progress': progress_data.get('research_progress'),
            'updated_at': datetime.utcnow()
        }
        
        result = self.db['StudentProfiles'].update_one(
            {'username': username},
            {'$push': {'academic_progress': progress}}
        )
        return result.modified_count > 0

    def create_researcher_profile(self, username, profile_data):
        """Create or update a researcher profile"""
        try:
            profile = {
                'username': username,
                'personal_info': {
                    'full_name': profile_data.get('full_name'),
                    'student_id': profile_data.get('student_id'),
                    'email': profile_data.get('email'),
                    'phone': profile_data.get('phone'),
                    'profile_picture': profile_data.get('profile_picture')
                },
                'academic_info': {
                    'university': profile_data.get('university'),
                    'department': profile_data.get('department'),
                    'position': profile_data.get('position'),
                    'specialization': profile_data.get('specialization'),
                    'research_areas': profile_data.get('research_areas', [])
                },
                'research_work': {
                    'current_projects': profile_data.get('current_projects', []),
                    'publications': profile_data.get('publications', []),
                    'research_interests': profile_data.get('research_interests', []),
                    'thesis_topic': profile_data.get('thesis_topic')
                },
                'education': profile_data.get('education', []),
                'achievements': profile_data.get('achievements', []),
                'updated_at': datetime.utcnow()
            }
            
            result = self.db['ResearcherProfiles'].update_one(
                {'username': username},
                {'$set': profile},
                upsert=True
            )
            return True, "Profile updated successfully"
        except Exception as e:
            return False, str(e)

    def get_researcher_profile(self, username):
        """Get researcher profile by username"""
        try:
            return self.db['ResearcherProfiles'].find_one({'username': username})
        except Exception as e:
            print(f"Error retrieving researcher profile: {e}")
            return None

    def update_research_work(self, username, work_data):
        """Update research work information"""
        try:
            update_data = {
                'research_work.current_projects': work_data.get('current_projects', []),
                'research_work.publications': work_data.get('publications', []),
                'research_work.research_interests': work_data.get('research_interests', []),
                'updated_at': datetime.utcnow()
            }
            
            result = self.db['ResearcherProfiles'].update_one(
                {'username': username},
                {'$set': update_data}
            )
            return True, "Research work updated successfully"
        except Exception as e:
            return False, str(e)

    def add_education_detail(self, username, education_data):
        """Add education detail to profile"""
        try:
            education = {
                'degree': education_data.get('degree'),
                'institution': education_data.get('institution'),
                'field': education_data.get('field'),
                'year': education_data.get('year'),
                'achievements': education_data.get('achievements', [])
            }
            
            result = self.db['ResearcherProfiles'].update_one(
                {'username': username},
                {'$push': {'education': education}}
            )
            return True, "Education detail added successfully"
        except Exception as e:
            return False, str(e)

    def add_library_resource(self, resource_data):
        """Add a new resource to the library"""
        try:
            resource = {
                'title': resource_data.get('title'),
                'author': resource_data.get('author'),
                'description': resource_data.get('description'),
                'file_path': resource_data.get('file_path'),
                'uploaded_by': resource_data.get('uploaded_by'),
                'upload_date': datetime.utcnow(),
                'category': resource_data.get('category'),
                'tags': resource_data.get('tags', []),
                'available': True
            }
            
            result = self.library_collection.insert_one(resource)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error adding resource: {e}")
            return None

    def get_library_resources(self, limit=None, skip=0):
        """Get all library resources"""
        try:
            query = self.library_collection.find().sort('upload_date', -1).skip(skip)
            if limit:
                query = query.limit(limit)
            return list(query)
        except Exception as e:
            print(f"Error retrieving resources: {e}")
            return []

    def search_library_resources(self, search_query):
        """Search library resources by title or author"""
        try:
            return list(self.library_collection.find({
                '$or': [
                    {'title': {'$regex': search_query, '$options': 'i'}},
                    {'author': {'$regex': search_query, '$options': 'i'}},
                    {'description': {'$regex': search_query, '$options': 'i'}}
                ]
            }))
        except Exception as e:
            print(f"Error searching resources: {e}")
            return []
