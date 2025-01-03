from flask import Flask, render_template, request, redirect, url_for, session, flash
from db import Database
import os

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')
app.secret_key = os.urandom(24)  # Required for session management
db = Database()

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/collaboration.html')
def collaboration():
    online_users = db.get_online_users()
    return render_template('collaboration.html', online_users=online_users)

@app.route('/data-analysis.html')
def data_analysis():
    return render_template('data-analysis.html')

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

if __name__ == '__main__':
    app.run(debug=True)
