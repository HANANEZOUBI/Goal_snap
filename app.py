from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

USERS_FILE = 'users.json'
TASKS_FILE = 'tasks.json'

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as file:
        return json.load(file)

def save_users(users):
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=4)

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as file:
        return json.load(file)

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        users = load_users()
        
        if username in users:
            flash('Username already exists!', 'danger')
            return redirect(url_for('signup'))
        
        users[username] = password
        save_users(users)
        
        flash('You have successfully signed up!', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        users = load_users()
        
        if username not in users or users[username] != password:
            flash('Invalid username or password!', 'danger')
            return redirect(url_for('login'))
        
        session['username'] = username
        flash('You have successfully logged in!', 'success')
        return redirect(url_for('project'))
    
    return render_template('login.html')

@app.route('/project')
def project():
    if 'username' in session:
        username = session['username']
        tasks = load_tasks()
        return render_template('project.html', username=username, tasks=tasks)
    else:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('login'))

@app.route('/update_task', methods=['POST'])
def update_task():
    if 'username' in session:
        tasks = load_tasks()
        task_id = int(request.form['task_id'])
        task_status = request.form['task_status'] == 'true'
        tasks[task_id]['done'] = task_status
        save_tasks(tasks)
        return jsonify({'success': True})
    return jsonify({'success': False}), 403

@app.route('/add_task', methods=['POST'])
def add_task():
    if 'username' in session:
        title = request.form['title']
        tasks = load_tasks()
        tasks.append({'title': title, 'done': False})
        save_tasks(tasks)
        return jsonify({'success': True})
    return jsonify({'success': False}), 403

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have successfully logged out!', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
