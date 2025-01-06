from db import Database
from datetime import datetime
import sys

def run_comprehensive_test():
    try:
        db = Database()
        tests = {
            'connection': test_connection(db),
            'write': test_write(db),
            'read': test_read(db),
            'update': test_update(db),
            'delete': test_delete(db)
        }
        
        print("\nTest Results:")
        for test_name, result in tests.items():
            status = "✅ Passed" if result else "❌ Failed"
            print(f"{test_name}: {status}")
            
    except Exception as e:
        print(f"Test failed with error: {e}")

def test_connection(db):
    try:
        db.client.admin.command('ping')
        print("Connection test: Success")
        return True
    except:
        print("Connection test: Failed")
        return False

def test_write(db):
    try:
        test_user = {
            'username': 'test_user',
            'password': 'test_password',
            'created_at': datetime.utcnow()
        }
        db.login_collection.insert_one(test_user)
        print("Write test: Success")
        return True
    except:
        print("Write test: Failed")
        return False

def test_read(db):
    try:
        user = db.login_collection.find_one({'username': 'test_user'})
        if user:
            print("Read test: Success")
            return True
        print("Read test: Failed - User not found")
        return False
    except:
        print("Read test: Failed")
        return False

def test_update(db):
    try:
        result = db.login_collection.update_one(
            {'username': 'test_user'},
            {'$set': {'last_login': datetime.utcnow()}}
        )
        if result.modified_count > 0:
            print("Update test: Success")
            return True
        print("Update test: Failed - No document updated")
        return False
    except:
        print("Update test: Failed")
        return False

def test_delete(db):
    try:
        result = db.login_collection.delete_one({'username': 'test_user'})
        if result.deleted_count > 0:
            print("Delete test: Success")
            return True
        print("Delete test: Failed - No document deleted")
        return False
    except:
        print("Delete test: Failed")
        return False

if __name__ == "__main__":
    run_comprehensive_test() 