from flask import Flask, render_template

app = Flask(__name__,
            template_folder='templates',
                static_folder='static')

# Routes for different pages
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/collaboration.html')
def collaboration():
    return render_template('collaboration_template.html')

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

@app.route('/login.html')
def login():
    return render_template('login.html')

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

if __name__ == "__main__":
    app.run(debug=True)
