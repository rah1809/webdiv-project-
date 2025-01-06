from db import Database
from datetime import datetime

def init_database():
    db = Database()
    
    # Test connection
    if not db.test_connection():
        print("Failed to connect to database")
        return

    # Create sample data
    try:
        # Clear existing data (be careful with this in production!)
        for collection in db.collections.values():
            collection.drop()

        # Create sample user
        admin_user = {
            'username': 'admin',
            'password': db.generate_password_hash('admin123'),
            'created_at': datetime.utcnow(),
            'is_active': True,
            'role': 'admin'
        }
        db.collections['login'].insert_one(admin_user)

        # Create sample profile
        admin_profile = {
            'username': 'admin',
            'email': 'admin@example.com',
            'full_name': 'Admin User',
            'department': 'Computer Science',
            'created_at': datetime.utcnow(),
            'research_interests': ['Data Analysis', 'Machine Learning']
        }
        db.collections['profiles'].insert_one(admin_profile)

        print("Database initialized successfully!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")

if __name__ == "__main__":
    init_database() 