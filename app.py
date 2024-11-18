from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import sqlite3

app = Flask(__name__)

# Initialize the SQLite3 database
def init_db():
    with sqlite3.connect('signed_colleges.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS signed_colleges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                college_name TEXT NOT NULL,
                principal_name TEXT NOT NULL,
                evidence_of_principalship TEXT NOT NULL
            )
        ''')
        conn.commit()

# Home route to display the form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        college_name = request.form['college_name']
        principal_name = request.form['principal_name']
        evidence_of_principalship = request.form['evidence_of_principalship']
        
        # Save to the database
        with sqlite3.connect('signed_colleges.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO signed_colleges (college_name, principal_name, evidence_of_principalship)
                VALUES (?, ?, ?)
            ''', (college_name, principal_name, evidence_of_principalship))
            conn.commit()
        
        return redirect(url_for('index'))
    
    return render_template('index.html')

# Route to display only college names
@app.route('/colleges')
def colleges():
    with sqlite3.connect('signed_colleges.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT college_name FROM signed_colleges')
        colleges = cursor.fetchall()  # Fetch all college names as a list of tuples
    return render_template('signed_colleges.html', colleges=[c[0] for c in colleges])  # Pass names to template

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/charter')
def charter():
    return render_template('charter.html')

@app.route('/files/<filename>')
def files(filename):
    return send_from_directory('static/files', filename)

if __name__ == '__main__':
    # Initialize the database when the app starts
    init_db()
    app.run(debug=True)
