from flask import render_template
from models.dashboard import get_user_data, get_user_analyses, get_recent_activities

@app.route('/dashboard')
def dashboard():
    # Assuming you have user authentication and can get user_id
    user_id = get_current_user_id()  # You'll need to implement this based on your auth system
    
    user_data = get_user_data(user_id)
    analyses = get_user_analyses(user_id)
    recent_activities = get_recent_activities(user_id)
    
    return render_template('dashboard.html',
                         user_data=user_data,
                         analyses=analyses,
                         recent_activities=recent_activities) 