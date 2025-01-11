from db import Database

def test_db_connection():
    try:
        # Initialize database
        db = Database()
        
        # Test connection
        print("Testing MongoDB connection...")
        
        # Ping the database
        db.client.admin.command('ping')
        print("✅ Successfully connected to MongoDB!")
        
        # Print database information
        print("\nDatabase Information:")
        print(f"Database name: {db.db.name}")
        print("\nCollections:")
        for collection in db.db.list_collection_names():
            print(f"- {collection}")
            # Print sample count
            count = db.db[collection].count_documents({})
            print(f"  Documents: {count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_db_connection() 