from flask import Flask, request, render_template, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash  # Import for password hashing

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session handling

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",  
    user="root",
    password="Sadhana@04",
    database="mindquest_db",
    port="3307"
)
cursor = db.cursor()

# ✅ Set Home Page as the Default Route
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user[2], password):  # Assuming password is stored in the 3rd column
            session['user'] = email  # Store user session
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials. Try again.", 'error')  # Flash message on failed login
            return redirect(url_for('login'))

    return render_template('login.html')

# Signup Route
# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match.", 'error')
            return redirect(url_for('signup'))

        # Check if email already exists
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("Email already registered.", 'error')
            return redirect(url_for('signup'))

        # Hash the password before saving it
        hashed_password = generate_password_hash(password)

        # Insert the new user into the database with the username
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                       (username, email, hashed_password))
        db.commit()

        flash("Registration successful! Please log in.", 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')


# Logout Route
@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove user session
    return redirect(url_for('home'))  # Redirect to home page after logout

@app.route('/about')
def about():
    return render_template('about.html')  # Make sure about.html exists in templates/

@app.route('/contact')
def contact():
    return render_template('contact.html')  # Ensure 'contact.html' exists in the templates folder

@app.route('/brick_breaker')  
def brick_breaker():
    return render_template('brick_breaker.html')

@app.route('/cross_road')  
def cross_road():
    return render_template('cross_road.html')

@app.route('/flappy_cube')  
def flappy_cube():
    return render_template('flappy_cube.html')

@app.route('/snake_game')  
def snake_game():
    return render_template('snake_game.html')

if __name__ == '__main__':
    app.run(debug=True)
