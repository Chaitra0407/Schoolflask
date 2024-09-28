from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from flask_session import Session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Define admin credentials as a dictionary
ADMIN_CREDENTIALS = {
    'Admin': 'chai123',
    'chai': '12345'
}

# Initialize the database
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stu01 (
            name TEXT,
            mail TEXT,
            Gender TEXT,
            number INTEGER,
            message TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Route for the index page
@app.route('/')
def index():
    return render_template('index.html')

# Route for submitting the form
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    mail = request.form['mail']
    gender = request.form['Gender']
    phone = request.form['number']
    message = request.form['message']

    # Validate the appointment date
    

    # Insert the data into the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO stu01 (name, mail, Gender, number, message) VALUES (?, ?, ?, ?, ?)", (name, mail, gender, phone, message))
    conn.commit()
    conn.close()

    # Flash a success message
    return '<script>alert("ThankYou For Your Valid Time"); window.location.href = "{}";</script>'.format(url_for('index'))
# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == password:
            session['logged_in'] = True
            flash('Successfully logged in!')
            return redirect(url_for('result'))
        else:
            flash('Invalid credentials, please try again.')
            return redirect(url_for('login'))
    return render_template('login.html')

# Route for logging out
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out')
    return redirect(url_for('login'))

# Route for the result page
@app.route('/result')
def result():
    if not session.get('logged_in'):
        flash('You need to log in to access this page')
        return redirect(url_for('login'))
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM stu01')
    data = cursor.fetchall()
    conn.close()
    return render_template('result.html', data=data)

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)