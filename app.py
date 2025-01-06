from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from db import Database
import os

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')
app.secret_key = os.urandom(24)  # Required for session management
db = Database()

@app.route('/')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Get user data from database
    user_data = db.get_user_data(session['username'])
    # Get user's analyses
    analyses = db.get_user_analyses(session['username'])
    # Get recent activities or other dashboard data
    recent_activities = db.get_recent_activities(session['username'])
    
    return render_template('dashboard.html',
                         user_data=user_data,
                         analyses=analyses,
                         recent_activities=recent_activities)


@app.route('/collaboration.html')
def collaboration():
    online_users = db.get_online_users()
    return render_template('collaboration.html', online_users=online_users)

@app.route('/data-analysis.html', methods=['GET', 'POST'])
def data_analysis():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        data_type = request.form.get('data_type')
        
        try:
            analysis_id = db.add_analysis(
                username=session['username'],
                title=title,
                description=description,
                data_type=data_type
            )
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': True, 'analysis_id': analysis_id})
            else:
                flash('Analysis created successfully!')
                return redirect(url_for('data_analysis'))
                
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'message': str(e)})
            else:
                flash('Error creating analysis: ' + str(e))
                return redirect(url_for('data_analysis'))

    # Get user's analyses for display
    analyses = db.get_user_analyses(session['username'])
    return render_template('data-analysis.html', analyses=analyses)

@app.route('/data-analysis/<analysis_id>', methods=['DELETE'])
def delete_analysis_route(analysis_id):
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    try:
        success = db.delete_analysis(analysis_id, session['username'])
        return jsonify({
            'success': success,
            'message': 'Analysis deleted successfully' if success else 'Failed to delete analysis'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/data.html')
def data():
    return render_template('data.html')

@app.route('/group-research.html')
def group_research():
    return render_template('group-research.html')

@app.route('/library.html')
def library():
    return render_template('library.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login_post', methods=['GET', 'POST'])
def login_post():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if db.verify_user(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form.get('email')  # Optional field
        full_name = request.form.get('full_name')  # Optional field
        
        success, message = db.add_user(
            username=username,
            password=password,
            email=email,
            full_name=full_name
        )
        
        if success:
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        else:
            flash('Username already exists')
            return redirect(url_for('register'))
    
    return render_template('register.html')

@app.route('/project-management.html')
def project_management():
    return render_template('project-management.html')

@app.route('/research-profile.html')
def research_profile():
    return render_template('research-profile.html')

@app.route('/tlogin.html')
def tlogin():
    return render_template('tlogin.html')

@app.route('/tlog.html')
def tlog():
    return render_template('tlog.html')

@app.route('/tlogin_post', methods=['GET', 'POST'])
def tlogin_post():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if db.verify_user(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('tlogin'))
    
    return render_template('tlogin.html')

@app.route('/data-analysis/view/<analysis_id>')
def view_analysis_details(analysis_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    analysis = db.get_analysis_by_id(analysis_id)
    if not analysis:
        flash('Analysis not found')
        return redirect(url_for('data_analysis'))
    
    return render_template('analysis-details.html', analysis=analysis)

@app.route('/data-analysis/share/<analysis_id>')
def share_analysis(analysis_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Get collaborators from research group
    collaborators = db.get_user_collaborators(session['username'])
    analysis = db.get_analysis_by_id(analysis_id)
    
    return render_template('share-analysis.html', 
                         analysis=analysis,
                         collaborators=collaborators)

@app.route('/data-analysis/export/<analysis_id>')
def export_analysis(analysis_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    analysis = db.get_analysis_by_id(analysis_id)
    if not analysis:
        flash('Analysis not found')
        return redirect(url_for('data_analysis'))
    
    # Generate export data
    export_data = db.prepare_analysis_export(analysis_id)
    return jsonify(export_data)

@app.route('/test-db')
def test_db():
    try:
        # Test basic connection
        db.client.admin.command('ping')
        
        # Get collection stats
        stats = {
            'database': db.db.name,
            'collections': {}
        }
        
        for collection in db.db.list_collection_names():
            stats['collections'][collection] = db.db[collection].count_documents({})
        
        return jsonify({
            'status': 'success',
            'message': 'Database connection successful',
            'stats': stats
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Database connection failed: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
