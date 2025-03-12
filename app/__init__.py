from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Database setup
def init_db():
    conn = sqlite3.connect('wiki.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS pages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            content TEXT NOT NULL,
            last_modified TEXT NOT NULL,
            author_id INTEGER,
            FOREIGN KEY (author_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()

# Initialize database
init_db()

# Utility function to get database connection
def get_db_connection():
    conn = sqlite3.connect('wiki.db')
    conn.row_factory = sqlite3.Row
    return conn

# Routes
@app.route('/')
def home():
    conn = get_db_connection()
    pages = conn.execute('SELECT * FROM pages ORDER BY last_modified DESC').fetchall()
    conn.close()
    return render_template('home.html', pages=pages)

@app.route('/page/<int:page_id>')
def view_page(page_id):
    conn = get_db_connection()
    page = conn.execute('SELECT * FROM pages WHERE id = ?', (page_id,)).fetchone()
    conn.close()
    if page is None:
        flash('Page not found.')
        return redirect(url_for('home'))
    return render_template('view_page.html', page=page)

@app.route('/create', methods=['GET', 'POST'])
def create_page():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author_id = 1  # Replace with current user ID
        last_modified = datetime.utcnow().isoformat()

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO pages (title, content, last_modified, author_id) VALUES (?, ?, ?, ?)',
                         (title, content, last_modified, author_id))
            conn.commit()
            conn.close()
            return redirect(url_for('home'))
        except sqlite3.Error as e:
            flash('Error creating page: {}'.format(e))
            conn.close()
            return redirect(url_for('create_page'))
    return render_template('create_page.html')

@app.route('/edit/<int:page_id>', methods=['GET', 'POST'])
def edit_page(page_id):
    conn = get_db_connection()
    page = conn.execute('SELECT * FROM pages WHERE id = ?', (page_id,)).fetchone()
    if page is None:
        flash('Page not found.')
        conn.close()
        return redirect(url_for('home'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        last_modified = datetime.utcnow().isoformat()

        try:
            conn.execute('UPDATE pages SET title = ?, content = ?, last_modified = ? WHERE id = ?',
                         (title, content, last_modified, page_id))
            conn.commit()
            conn.close()
            return redirect(url_for('view_page', page_id=page_id))
        except sqlite3.Error as e:
            flash('Error updating page: {}'.format(e))
            conn.close()
            return redirect(url_for('edit_page', page_id=page_id))
    conn.close()
    return render_template('edit_page.html', page=page)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
