from pymongo import MongoClient
from datetime import datetime, timedelta
import random

def connect_db():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['ResearchDB']
    return db

def add_test_data():
    db = connect_db()
    
    # Clear existing data
    db['UserProfiles'].delete_many({})
    db['DataAnalysis'].delete_many({})
    db['Projects'].delete_many({})
    db['UserActivities'].delete_many({})
    db['ResearchGroups'].delete_many({})
    
    # Create test user profiles
    test_users = [
        {
            'username': '62200581',
            'email': 'test1@example.com',
            'full_name': 'Test User One',
            'department': 'Computer Science',
            'created_at': datetime.utcnow(),
            'research_interests': ['AI', 'Machine Learning', 'Data Science'],
            'profile_completed': True
        },
        {
            'username': 'test_user2',
            'email': 'test2@example.com',
            'full_name': 'Test User Two',
            'department': 'Data Science',
            'created_at': datetime.utcnow(),
            'research_interests': ['Big Data', 'Analytics'],
            'profile_completed': True
        }
    ]
    
    db['UserProfiles'].insert_many(test_users)
    
    # Create test analyses
    analyses = [
        {
            'username': '62200581',
            'title': 'Machine Learning Analysis',
            'description': 'Analysis of ML algorithms performance',
            'data_type': 'quantitative',
            'created_at': datetime.utcnow() - timedelta(days=5),
            'updated_at': datetime.utcnow(),
            'status': 'completed',
            'results': {'accuracy': 0.95, 'precision': 0.92}
        },
        {
            'username': '62200581',
            'title': 'Data Mining Study',
            'description': 'Exploratory data analysis',
            'data_type': 'mixed',
            'created_at': datetime.utcnow() - timedelta(days=2),
            'updated_at': datetime.utcnow(),
            'status': 'in_progress',
            'results': None
        }
    ]
    
    db['DataAnalysis'].insert_many(analyses)
    
    # Create test projects
    projects = [
        {
            'title': 'AI Research Project',
            'description': 'Research on AI applications',
            'created_by': '62200581',
            'team_members': ['62200581', 'test_user2'],
            'start_date': datetime.utcnow() - timedelta(days=30),
            'end_date': datetime.utcnow() + timedelta(days=60),
            'status': 'active',
            'progress': 45
        },
        {
            'title': 'Data Analysis Project',
            'description': 'Big data analysis project',
            'created_by': 'test_user2',
            'team_members': ['62200581', 'test_user2'],
            'start_date': datetime.utcnow() - timedelta(days=15),
            'end_date': datetime.utcnow() + timedelta(days=45),
            'status': 'active',
            'progress': 30
        }
    ]
    
    db['Projects'].insert_many(projects)
    
    # Create test activities
    activities = []
    activity_types = ['login', 'analysis_created', 'project_updated', 'file_uploaded']
    
    for _ in range(10):
        activity = {
            'username': random.choice(['62200581', 'test_user2']),
            'activity_type': random.choice(activity_types),
            'description': f'Test activity description {_}',
            'created_at': datetime.utcnow() - timedelta(days=random.randint(0, 10)),
            'details': {
                'location': 'Research Lab',
                'device': 'Desktop'
            }
        }
        activities.append(activity)
    
    db['UserActivities'].insert_many(activities)
    
    # Create test research groups
    research_groups = [
        {
            'name': 'AI Research Group',
            'description': 'Research group focused on AI',
            'members': ['62200581', 'test_user2'],
            'created_at': datetime.utcnow(),
            'leader': '62200581',
            'active_projects': 2
        },
        {
            'name': 'Data Science Group',
            'description': 'Data science research group',
            'members': ['test_user2'],
            'created_at': datetime.utcnow(),
            'leader': 'test_user2',
            'active_projects': 1
        }
    ]
    
    db['ResearchGroups'].insert_many(research_groups)
    
    print("Test data added successfully!")
    
    # Print summary
    print("\nData Summary:")
    print(f"Users: {db['UserProfiles'].count_documents({})}")
    print(f"Analyses: {db['DataAnalysis'].count_documents({})}")
    print(f"Projects: {db['Projects'].count_documents({})}")
    print(f"Activities: {db['UserActivities'].count_documents({})}")
    print(f"Research Groups: {db['ResearchGroups'].count_documents({})}")

def main():
    try:
        add_test_data()
    except Exception as e:
        print(f"Error adding test data: {e}")

if __name__ == "__main__":
    main() 