# Database configuration
MONGODB_CONFIG = {
    'host': 'localhost',
    'port': 27017,
    'db_name': 'ResearchDB',
    'collections': {
        'users': 'Users',
        'login': 'Login',
        'profiles': 'UserProfiles',
        'analyses': 'DataAnalysis',
        'groups': 'ResearchGroups',
        'projects': 'Projects',
        'publications': 'Publications',
        'online_users': 'OnlineUsers'
    }
}

# Collection schemas
SCHEMAS = {
    'users': {
        'username': str,
        'email': str,
        'password': str,
        'created_at': datetime,
        'last_login': datetime,
        'is_active': bool
    },
    'profiles': {
        'username': str,
        'full_name': str,
        'department': str,
        'research_interests': list,
        'publications': list,
        'projects': list
    },
    'analyses': {
        'title': str,
        'description': str,
        'data_type': str,
        'created_by': str,
        'created_at': datetime,
        'updated_at': datetime,
        'status': str,
        'results': dict
    }
} 