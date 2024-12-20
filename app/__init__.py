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
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    # Blog pages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blogs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            creator_username TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT (datetime('now','localtime')),
            FOREIGN KEY (creator_username) REFERENCES users(username)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Home page route showing all posts
@app.route('/')
def main():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user."""
    if request.method == 'POST':  # Process form data
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("Username and password are required.", "danger")
            return redirect('/register')

        try:
            # Insert new user into the database with plain text password
            with sqlite3.connect('db.sqlite3') as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
                conn.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect('/login')
        except sqlite3.IntegrityError:
            flash("Username already exists. Choose a different one.", "danger")
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
            flash("Username and password are required.", "danger")
            return redirect('/login')

        # Validate user credentials directly against the plain text password
        with sqlite3.connect('db.sqlite3') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
            result = cursor.fetchone()

        if result:
            # Username exists, now check if the password matches
            if result[0] == password:
                session['username'] = username  # Store user in session
                return redirect('/home')
            else:
                flash("Incorrect password. Please try again.", "danger")
                return redirect('/login')
        else:
            # Username does not exist, redirect to registration
            flash("Username not found. Please register first.", "danger")
            return redirect('/register')

    # Render login page if GET request
    return render_template("login.html")

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect('/login')
    with sqlite3.connect('db.sqlite3') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, creator_username, created_at FROM blogs ORDER BY created_at DESC')
        posts = cursor.fetchall()

    blogs = [{'id': post[0], 'title': post[1], 'creator_username': post[2], 'created_at': post[3]} for post in posts]
    curr_user = session['username']
    return render_template('home.html', blogs=blogs, cUser = curr_user)

# ------ Unused Code ------
@app.route('/myblogs')
def my_blogs():
    if 'username' not in session:
        return redirect('/login')
    with sqlite3.connect('db.sqlite3') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, created_at FROM blogs ORDER BY created_at DESC WHERE creator_username = ?',
                       (session['username']))
        posts = cursor.fetchall()

    blogs = [{'id': post[0], 'title': post[1], 'created_at': post[2]} for post in posts]

    return render_template('my_blogs.html', blogs=blogs)
# ------ Unused Code ------

@app.route('/logout')
def logout():
    # Clear the user session if logged in
    session.pop('username', None)
    return redirect('/register')

# Route to create a new blog post
@app.route('/create', methods=['GET', 'POST'])
def create_blog():
    if 'username' not in session:
        return redirect('/login')

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        creator = session['username']

        with sqlite3.connect('db.sqlite3') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO blogs (title, content, creator_username) VALUES (?, ?, ?)',
                           (title, content, creator))
            conn.commit()
        flash('Blog post created successfully!', 'success')
        return redirect('/home')
    curr_user = session['username']
    return render_template('create.html', cUser = curr_user)


# catch
@app.route('/edit', methods=['GET', 'POST'])
def back():
    if request.method == 'POST':
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        new_title = request.form['title']
        new_content = request.form['content']
        edit_id = request.form['id']

        # Update the blog post
        cursor.execute('UPDATE blogs SET title = ?, content = ? WHERE id = ?', (new_title, new_content, edit_id))
        conn.commit()
        conn.close()
        flash('Blog post updated successfully!', 'success')
        return redirect('/home')
    else:
        return redirect('/home')

# Route to edit an existing blog post
@app.route('/edit/<int:post_id>')
def edit_blog(post_id):
    if 'username' not in session:
        return redirect("/login")

    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    # Fetch existing content
    cursor.execute('SELECT title, content, id FROM blogs WHERE id = ?', (post_id, ))
    post = cursor.fetchone()

    conn.close()
    curr_user = session['username']
    return render_template('edit.html', post=post, cUser = curr_user)

# Route to view a single blog post
@app.route('/post/<int:post_id>')
def view_blog(post_id):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('SELECT title, content, creator_username, created_at FROM blogs WHERE id = ?', (post_id,))
    post = cursor.fetchone()
    conn.close()
    return render_template('view.html', post=post)

# Run the app
if __name__ == "__main__":
    app.debug = True
    app.run()
