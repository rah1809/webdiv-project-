from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file
from db import Database
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')
app.secret_key = os.urandom(24)  # Required for session management

# Initialize database
db = Database()

@app.route('/')
@app.route('/login')
def login():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

def db_required(f):
    """Decorator to ensure database is connected"""
    def wrapper(*args, **kwargs):
        if not db.is_connected():
            flash('Database is not connected. Please try again later.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route('/login_post', methods=['GET', 'POST'])
@db_required
def login_post():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            if db.verify_user(username, password):
                session['username'] = username
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password')
                return redirect(url_for('login'))
        except Exception as e:
            flash('Error during login. Please try again.')
            return redirect(url_for('login'))
    
    return render_template('login.html')

# Add the decorator to all routes that need database access
@app.route('/dashboard')
@db_required
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    try:
        user_data = db.get_user_data(session['username'])
        analyses = db.get_user_analyses(session['username'])
        recent_activities = db.get_recent_activities(session['username'])
        
        return render_template('dashboard.html',
                             user_data=user_data,
                             analyses=analyses,
                             recent_activities=recent_activities)
    except Exception as e:
        flash('Error loading dashboard data')
        return render_template('dashboard.html',
                             user_data={},
                             analyses=[],
                             recent_activities=[])

@app.route('/collaboration.html')
def collaboration():
    online_users = db.get_online_users()
    return render_template('collaboration.html', online_users=online_users)

@app.route('/data-analysis', methods=['GET', 'POST'])
def data_analysis():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        data_type = request.form.get('data_type')
        
        # Handle file upload
        if 'data_file' not in request.files:
            message = 'No file uploaded'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'message': message})
            flash(message)
            return redirect(request.url)
            
        file = request.files['data_file']
        if file.filename == '':
            message = 'No file selected'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'message': message})
            flash(message)
            return redirect(request.url)
            
        if file:
            try:
                # Create uploads directory if it doesn't exist
                upload_dir = os.path.join('static', 'uploads', 'analysis')
                os.makedirs(upload_dir, exist_ok=True)
                
                # Secure the filename and save the file
                filename = secure_filename(file.filename)
                file_path = os.path.join(upload_dir, filename)
                file.save(file_path)
                
                # Add to database
                analysis_id = db.add_analysis(
                    username=session['username'],
                    title=title,
                    description=description,
                    data_type=data_type,
                    file_path=file_path
                )
                
                message = 'Analysis created successfully!'
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({
                        'success': True,
                        'message': message,
                        'analysis_id': analysis_id
                    })
                    
                flash(message)
                return redirect(url_for('data_analysis'))
                    
            except Exception as e:
                message = f'Error creating analysis: {str(e)}'
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({'success': False, 'message': message})
                flash(message)
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
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Get all library resources
    resources = db.get_library_resources()
    return render_template('library.html', resources=resources)

@app.route('/library/search')
def search_library():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    query = request.args.get('q', '')
    resources = db.search_library_resources(query)
    return jsonify(resources)

@app.route('/library/add', methods=['POST'])
def add_library_resource():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    try:
        file = request.files['file']
        if file:
            # Create uploads directory if it doesn't exist
            upload_dir = os.path.join('static', 'uploads', 'library')
            os.makedirs(upload_dir, exist_ok=True)
            
            # Save the file
            filename = secure_filename(file.filename)
            file_path = os.path.join(upload_dir, filename)
            file.save(file_path)
        else:
            file_path = None

        # Prepare resource data
        resource_data = {
            'title': request.form.get('title'),
            'author': request.form.get('author'),
            'description': request.form.get('description'),
            'file_path': file_path,
            'uploaded_by': session['username'],
            'category': request.form.get('category'),
            'tags': request.form.get('tags', '').split(',')
        }
        
        # Add resource to database
        resource_id = db.add_library_resource(resource_data)
        
        if resource_id:
            return jsonify({'success': True, 'message': 'Resource added successfully'})
        return jsonify({'success': False, 'message': 'Failed to add resource'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form.get('email')
        full_name = request.form.get('full_name')
        security_question = request.form.get('security-question')
        security_answer = request.form.get('security-answer')
        
        # Validate required fields
        if not all([username, password, email, security_question, security_answer]):
            flash('All required fields must be filled out')
            return redirect(url_for('register'))
        
        # Add user and get result
        success, message = db.add_user(
            username=username,
            password=password,
            email=email,
            full_name=full_name
        )
        
        if success:
            # Set security question
            db.set_security_question(email, security_question, security_answer)
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        else:
            flash(message)
            return redirect(url_for('register'))
    
    return render_template('register.html')

@app.route('/project-management.html', methods=['GET', 'POST'])
def project_management():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Simply render the under construction page
    return render_template('project-management.html')

@app.route('/project/<project_id>', methods=['GET'])
def view_project(project_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    project = db.get_project(project_id)
    if not project:
        flash('Project not found')
        return redirect(url_for('project_management'))
    
    return render_template('project-details.html', project=project)

@app.route('/project/<project_id>/update', methods=['POST'])
def update_project(project_id):
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    update_data = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'start_date': request.form.get('start_date'),
        'end_date': request.form.get('end_date'),
        'status': request.form.get('status'),
        'team_members': request.form.getlist('team_members')
    }
    
    success, message = db.update_project(project_id, update_data)
    return jsonify({'success': success, 'message': message})

@app.route('/project/<project_id>/task', methods=['POST'])
def add_project_task(project_id):
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    task_data = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'assigned_to': request.form.get('assigned_to'),
        'due_date': request.form.get('due_date'),
        'priority': request.form.get('priority')
    }
    
    success = db.add_project_task(project_id, task_data)
    return jsonify({'success': success})

@app.route('/project/<project_id>/status', methods=['POST'])
def update_project_status(project_id):
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    status = request.form.get('status')
    success = db.update_project_status(project_id, status)
    return jsonify({'success': success})

@app.route('/research-profile', methods=['GET', 'POST'])
def research_profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        profile_data = {
            'researcher_id': request.form.get('researcher_id'),
            'academic_position': request.form.get('academic_position'),
            'research_group': request.form.get('research_group'),
            'projects': request.form.getlist('projects'),
            'research_topic': request.form.get('research_topic')
        }
        
        success, message = db.create_researcher_profile(session['username'], profile_data)
        if success:
            flash('Profile updated successfully!')
        else:
            flash('Error updating profile: ' + message)
    
        return redirect(url_for('research_profile'))
    
    # Get existing profile data and projects list
    profile = db.get_researcher_profile(session['username'])
    projects = db.get_available_projects()  # You'll need to implement this in your Database class
    
    return render_template('research-profile.html', profile=profile, projects=projects)

@app.route('/add-education', methods=['POST'])
def add_education():
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    education_data = {
        'degree': request.form.get('degree'),
        'institution': request.form.get('institution'),
        'field': request.form.get('field'),
        'year': request.form.get('year'),
        'achievements': request.form.getlist('achievements')
    }
    
    success, message = db.add_education_detail(session['username'], education_data)
    return jsonify({'success': success, 'message': message})

@app.route('/update-research', methods=['POST'])
def update_research():
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    work_data = {
        'current_projects': request.form.getlist('current_projects'),
        'publications': request.form.getlist('publications'),
        'research_interests': request.form.getlist('research_interests')
    }
    
    success, message = db.update_research_work(session['username'], work_data)
    return jsonify({'success': success, 'message': message})

@app.route('/add-research-topic', methods=['POST'])
def add_research_topic():
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    topic_data = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'category': request.form.get('category'),
        'status': request.form.get('status'),
        'start_date': request.form.get('start_date'),
        'supervisor': request.form.get('supervisor')
    }
    
    success = db.add_research_topic(session['username'], topic_data)
    if success:
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Failed to add research topic'})

@app.route('/update-academic-progress', methods=['POST'])
def update_academic_progress():
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    progress_data = {
        'semester': request.form.get('semester'),
        'gpa': request.form.get('gpa'),
        'completed_credits': request.form.get('completed_credits'),
        'research_progress': request.form.get('research_progress')
    }
    
    success = db.update_academic_progress(session['username'], progress_data)
    if success:
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Failed to update progress'})

@app.route('/add-publication', methods=['POST'])
def add_publication():
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    publication_data = {
        'title': request.form.get('title'),
        'authors': request.form.getlist('authors'),
        'journal': request.form.get('journal'),
        'year': request.form.get('year'),
        'doi': request.form.get('doi')
    }
    
    success = db.add_publication(session['username'], publication_data)
    if success:
        db.update_research_stats(session['username'])
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Failed to add publication'})

@app.route('/add-project', methods=['POST'])
def add_project():
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    project_data = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'start_date': request.form.get('start_date'),
        'end_date': request.form.get('end_date'),
        'collaborators': request.form.getlist('collaborators'),
        'funding': request.form.get('funding')
    }
    
    success = db.add_research_project(session['username'], project_data)
    if success:
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Failed to add project'})

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

@app.route('/library/cite/<resource_id>')
def get_citation(resource_id):
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    try:
        resource = db.get_library_resource(resource_id)
        if not resource:
            return jsonify({'success': False, 'message': 'Resource not found'})
        
        # Format citation in APA style
        # Author. (Year). Title. Publisher. URL
        citation = ""
        
        # Add authors
        if resource.get('author'):
            citation += f"{resource['author']}. "
        
        # Add date in parentheses
        pub_date = resource.get('publication_date', resource.get('upload_date'))
        if pub_date:
            year = pub_date.year if isinstance(pub_date, datetime) else 'n.d.'
            citation += f"({year}). "
        
        # Add title
        if resource.get('title'):
            citation += f"{resource['title']}. "
        
        # Add publisher
        if resource.get('publisher'):
            citation += f"{resource['publisher']}. "
        
        # Add URL if available
        if resource.get('url'):
            citation += f"Retrieved from {resource['url']}"
        
        return jsonify({
            'success': True,
            'citation': citation.strip()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error generating citation: {str(e)}'
        })

@app.route('/search-researchers')
def search_researchers():
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    query = request.args.get('q', '')
    researchers = db.search_researchers(query)
    return jsonify(researchers)

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        question = request.form.get('security-question')
        answer = request.form.get('security-answer')
        
        # Verify security answer
        if db.verify_security_answer(email, answer):
            # Generate reset token
            token = db.create_reset_token(email)
            
            # In a real application, you would send this token via email
            # For now, we'll redirect to the reset page directly
            return redirect(url_for('reset_password', token=token))
        else:
            flash('Invalid email or security answer', 'error')
            return redirect(url_for('forgot_password'))
            
    return render_template('forgot-password.html')

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if new_password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('reset_password', token=token))
            
        if db.reset_password(token, new_password):
            flash('Password reset successful', 'success')
            return redirect(url_for('login'))
        else:
            flash('Invalid or expired reset token', 'error')
            return redirect(url_for('forgot_password'))
            
    # Verify token is valid before showing reset form
    email = db.verify_reset_token(token)
    if not email:
        flash('Invalid or expired reset token', 'error')
        return redirect(url_for('forgot_password'))
        
    return render_template('reset-password.html', token=token)

@app.route('/set-security-question', methods=['POST'])
def set_security_question():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
        
    email = session['user']['email']
    question = request.form.get('security-question')
    answer = request.form.get('security-answer')
    
    if db.set_security_question(email, question, answer):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Failed to set security question'})

@app.route('/api/messages', methods=['GET', 'POST'])
def handle_messages():
    if 'username' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    if request.method == 'GET':
        try:
            # Get the last 50 messages
            messages = db.get_chat_messages(limit=50)
            return jsonify(messages)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    elif request.method == 'POST':
        try:
            data = request.get_json()
            message = {
                'text': data.get('text'),
                'username': session['username'],
                'timestamp': datetime.utcnow()
            }
            
            # Save the message
            message_id = db.add_chat_message(message)
            if message_id:
                message['_id'] = str(message_id)
                return jsonify(message), 201
            else:
                return jsonify({'error': 'Failed to save message'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    if not db.is_connected():
        print("\nWARNING: Database is not connected!")
        print("The application will start, but functionality will be limited.")
        print("Please ensure MongoDB is running and restart the application.\n")
    app.run(debug=True, use_reloader=False)
