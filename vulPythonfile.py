import sqlite3
import os
import pickle
import subprocess
import yaml
from flask import Flask, request, render_template_string

app = Flask(__name__)

# 1. Hardcoded Sensitive Information (Credentials)
SECRET_KEY = "super_secret_password_123"

@app.route('/login', methods=['POST'])
def login():
    # 2. SQL Injection (SQLi)
    # User input is concatenated directly into the query
    username = request.form.get('username')
    db = sqlite3.connect("users.db")
    cursor = db.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query) 
    return "Logged in"

@app.route('/upload', methods=['POST'])
def upload_data():
    # 3. Insecure Deserialization (Pickle)
    # pickle.loads() on untrusted data can execute arbitrary code
    data = request.files['file'].read()
    user_obj = pickle.loads(data)
    return "Data processed"

@app.route('/ping')
def ping_host():
    # 4. OS Command Injection
    # Using shell=True with user input allows executing extra shell commands
    target = request.args.get('target')
    subprocess.call(f"ping -c 1 {target}", shell=True)
    return "Pinged!"

@app.route('/config')
def load_config():
    # 5. Insecure YAML Loading
    # yaml.load() is unsafe; it can instantiate any Python object
    user_config = request.args.get('cfg')
    config = yaml.load(user_config) 
    return "Config updated"

@app.route('/profile')
def profile():
    # 6. Cross-Site Scripting (XSS)
    # Rendering raw user input directly into HTML
    name = request.args.get('name', 'Guest')
    template = f"<h1>Welcome, {name}!</h1>"
    return render_template_string(template)

@app.route('/debug')
def debug_info():
    # 7. Sensitive Data Exposure (Path Traversal)
    # Allowing users to specify filenames can let them read /etc/passwd
    filename = request.args.get('file')
    with open(os.path.join("logs", filename), "r") as f:
        return f.read()

if __name__ == "__main__":
    app.run(debug=True) # Bonus: Debug mode enabled in production is a risk!
