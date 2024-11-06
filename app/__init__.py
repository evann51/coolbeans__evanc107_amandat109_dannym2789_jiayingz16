# Coolbeans: Evan, Michelle, Danny, Amanda

# Imports
from flask import Flask, redirect, render_template, session, request, flash
import sqlite3
import os

# Initialize the Flask app
app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = os.urandom(32)

# Database setup
def init_db():
    """Initialize the database with a users table if it doesn't already exist."""
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def recover_session():
    # Redirect to home if user is already logged in, otherwise to login
    return redirect('/home') if 'username' in session else redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user."""
    if request.method == 'POST':  # Process form data
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("Username and password are required.", "error")
            return redirect('/register')

        try:
            # Insert new user into the database with plain text password
            conn = sqlite3.connect('db.sqlite3')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            conn.close()

            flash("Registration successful! Please log in.", "success")
            return redirect('/login')
        except sqlite3.IntegrityError:
            flash("Username already exists. Choose a different one.", "error")
            return redirect('/register')

    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def user_login():
    # Redirect to home if session is active
    if 'username' in session:
        return redirect('/home')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if username and password are filled out
        if not username or not password:
            flash("Username and password are required.", "error")
            return redirect('/login')

        # Validate user credentials directly against the plain text password
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()  # Fetch the first row of tuple associated with username
        conn.close()

        if result:
            # Username exists, now check if the password matches
            if result[0] == password:
                session['username'] = username  # Store user in session
                return redirect('/home')
            else:
                flash("Incorrect password. Please try again.", "error")
                return redirect('/login')
        else:
            # Username does not exist, redirect to registration
            flash("Username not found. Please register first.", "error")
            return redirect('/register')

    # Render login page if GET request
    return render_template("login.html")

@app.route('/home')
def display_home():
    # Check if the user is logged in
    if 'username' not in session:
        return redirect('/login')
    return render_template("home.html")

@app.route('/logout')
def logout():
    # Clear the user session if logged in
    session.pop('username', None)
    return redirect('/')

# Run the app
if __name__ == "__main__":
    app.debug = True
    app.run()