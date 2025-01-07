from pymongo import MongoClient

def get_database():
    # Connect to MongoDB (update the connection string if needed)
    client = MongoClient('mongodb://localhost:27017/')
    
    # Create or get the database
    db = client['dashboard_db']
    return db 