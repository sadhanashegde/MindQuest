from flask import Flask, request, render_template, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session handling

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sm123",
    database="mindquest_db"
)
cursor = db.cursor()

# ✅ Set Home Page as the Default Route
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()

        if user:
            session['user'] = email  # Store user session
            return redirect(url_for('home'))
        else:
            return "Invalid credentials. Try again."

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')  # Make sure 'signup.html' exists in templates/

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
