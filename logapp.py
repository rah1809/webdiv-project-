from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_pymongo import PyMongo

app = Flask(__name__)

# MongoDB Configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/your_database_name"  # Replace with your DB name
mongo = PyMongo(app)

# Route for Login Page
@app.route('/')
def login():
    return render_template('login.html')

# Route for Login Authentication
@app.route('/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']

    # Check in MongoDB
    user = mongo.db.users.find_one({"username": username, "password": password})

    if user:
        return jsonify({"status": "success", "message": "Login Successful!"})
    else:
        return jsonify({"status": "fail", "message": "Invalid Username or Password!"})

# Route to Insert New User (optional)
@app.route('/register', methods=['POST'])
def register_user():
    data = {
        "username": request.form['username'],
        "password": request.form['password']
    }
    mongo.db.users.insert_one(data)
    return jsonify({"status": "success", "message": "User Registered!"})

if __name__ == "__main__":
    app.run(debug=True)
