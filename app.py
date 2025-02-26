from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Database setup
def init_db():
    with sqlite3.connect('instance/cases.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_name TEXT NOT NULL,
                status TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hearings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_id INTEGER,
                hearing_date TEXT NOT NULL,
                FOREIGN KEY (case_id) REFERENCES cases (id)
            )
        ''')
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Here you would normally check the credentials
        flash('Login successful!', 'success')
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect('instance/cases.db') as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
                conn.commit()
                flash('Registration successful!', 'success')
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                flash('Username already exists!', 'danger')
    return render_template('register.html')

@app.route('/case', methods=['GET', 'POST'])
def case():
    if request.method == 'POST':
        # Handle case addition here if needed
        pass
    return render_template('case.html')

@app.route('/add_case', methods=['GET', 'POST'])
def add_case():
    if request.method == 'POST':
        case_name = request.form['case_name']
        status = request.form['status']
        with sqlite3.connect('instance/cases.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO cases (case_name, status) VALUES (?, ?)', (case_name, status))
            conn.commit()
            flash('Case added successfully!', 'success')
            return redirect(url_for('case'))  # Redirect to the case page or wherever you want

    # If the request method is GET, render the add_case.html template
    return render_template('add_case.html')  # Ensure this template exists
    
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/hearings')
def hearings():
    return render_template('hearings.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)