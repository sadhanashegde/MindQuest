from flask import Flask, request, render_template, redirect, url_for, session, flash,jsonify
from flask_socketio import SocketIO, join_room, leave_room, emit
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import random
from utils.sentiment_analysis import analyze_sentiment  # Import analysis function

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session handling

# Setup SocketIO
socketio = SocketIO(app)

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",  
    user="root",
    password="shraddha8",
    database="mindquest_db"
    
)
cursor = db.cursor()

# ✅ Set Home Page as the Default Route
# ✅ Set Root Route to Redirect to Home
@app.route('/')
def index():
    return redirect(url_for('home'))  # Redirect '/' to '/home'

@app.route('/home')
def home():
    return render_template('home.html')


# Login Route
@app.route('/login', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor.execute("SELECT username, email, password FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user[2], password):  # Assuming password is stored in the 3rd column
            session['user'] = user[0]  # Save the username in the session (user[0] is the username)
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials. Try again.", 'error')
            return redirect(url_for('login'))

    return render_template('login.html')


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
    flash("You have been logged out.", 'success')
    return redirect(url_for('home'))  # Redirect to home page after logout

@app.route('/about')
def about():
    return render_template('about.html')  # Ensure about.html exists in templates/


@app.route('/sentiment_analysis', methods=['GET', 'POST'])
def sentiment_analysis():
    user_text = ""  # Ensure default value
    mood_result = None
    polarity = None
    points = None
    suggestions = None
    song_list = None
    stress_prediction = None

    if request.method == 'POST':
        user_text = request.form.get("text_input", "").strip()
        
        if user_text:
            # Perform sentiment analysis (Assuming you have this logic)
            mood_result, polarity, points, suggestions, song_list, stress_prediction = analyze_sentiment(user_text)

        else:
            mood_result = "neutral"

    return render_template(
        "sentiment_analysis.html",
        user_text=user_text,  # ✅ Always pass user text
        mood_result=mood_result,  # ✅ Always pass mood result
        polarity=polarity,
        points=points,
        suggestions=suggestions,
        song_list=song_list,
        stress_prediction=stress_prediction
    )


# Game Routes

@app.route('/mini_games')
def mini_games():
    return render_template('mini_games.html')  # Ensure 'mini_games.html' exists in /templates

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

# Chatroom Route (Only accessible when logged in)
@app.route('/chatroom')
def chatroom():
    if 'user' in session:
        username = session['user']  # Get the username from the session
        return render_template('chatroom.html', username=username)  # Pass the username to the template
    else:
        flash("You need to be logged in to access the chatroom.", 'error')
        return redirect(url_for('login'))

# SocketIO Events for Chatroom
@socketio.on('join_room')
def handle_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    emit('message', {'username': 'System', 'message': f"{username} has joined the room."}, to=room)

@socketio.on('leave_room')
def handle_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    emit('message', {'username': 'System', 'message': f"{username} has left the room."}, to=room)

@socketio.on('send_message')
def handle_message(data):
    username = data['username']
    room = data['room']
    message = data['message']
    emit('message', {'username': username, 'message': message}, to=room)


basic_chatbot_responses = {
    "hi": ["Hey! How can I help you?"],  # Modified response for "hi"
    "hello": ["Hi there!", "Hello! How can I help you?", "Hey! 😊"],
    "how are you": ["I'm just a bot, but I'm here to assist!", "I'm doing great! How about you?"],
    "what is your name": ["I'm MindQuest Bot!", "Call me MindQuest Assistant."],
    "bye": ["Goodbye! Take care. 💙", "See you soon!", "Bye! Have a great day!"],
}


# ✅ Mood-Based Responses
mental_health_responses = {
    "stress": [
        "I sense you're feeling stressed. Let's do a quick breathing exercise: 🫁\n"
        "1️⃣ Inhale deeply through your nose for **4 seconds**... \n"
        "2️⃣ Hold your breath for **4 seconds**... \n"
        "3️⃣ Exhale slowly through your mouth for **4 seconds**... \n"
        "Repeat this 5 times and notice how you feel. 💙",
        
        "Feeling stressed? Try this: 🌿 **Box Breathing Method** 🌿 \n"
        "Breathe in **4 seconds** ➡️ Hold **4 seconds** ➡️ Exhale **4 seconds** ➡️ Hold **4 seconds** \n"
        "Repeat for 1-2 minutes for a calming effect. 💙"
    ],
    "anxiety": [
        "Anxiety can be overwhelming. Try grounding yourself: \n"
        "👀 Name 5 things you see \n"
        "👂 Name 4 things you hear \n"
        "🤲 Name 3 things you can touch \n"
        "👃 Name 2 things you smell \n"
        "👅 Name 1 thing you taste \n"
        "This can help bring you to the present moment. 🌸",
    ],
    "sadness": [
        "It's okay to feel sad. I'm here for you. 💙 Maybe try journaling your thoughts to express your emotions?",
        "Sadness can be heavy. Try listening to calming music or doing something creative. Would you like a guided relaxation exercise?",
    ],
    "happiness": [
        "I'm so happy to hear that! 😃 Keep embracing positivity! Would you like to play a game to boost your mood even more?",
        "Happiness is wonderful! If you want to reflect on your emotions, journaling might be a great way to capture the moment.",
    ],
    "default": [
        "I'm here to support you. If you're feeling stressed, anxious, or down, let me know so I can help!",
        "Mental well-being is important. I can suggest relaxation exercises or mindfulness activities if you'd like.",
    ],
}

# ✅ Mood Detection Function
def detect_mood(message):
    message = message.lower()
    if any(word in message for word in ["stressed", "overwhelmed", "pressure"]):
        return "stress"
    elif any(word in message for word in ["anxious", "nervous", "panic"]):
        return "anxiety"
    elif any(word in message for word in ["sad", "depressed", "down"]):
        return "sadness"
    elif any(word in message for word in ["happy", "excited", "joyful"]):
        return "happiness"
    else:
        return "default"

# ✅ Chatbot Route
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").lower().strip()

    # First message from bot when user starts chat
    if not user_message:
        return jsonify({"response": "Hello! How may I help you today? 😊"})

    # Check if it's a basic question
    if user_message in basic_chatbot_responses:
        bot_reply = random.choice(basic_chatbot_responses[user_message])
    else:
        # Detect mood-based response
        mood = detect_mood(user_message)
        bot_reply = random.choice(mental_health_responses[mood])

    return jsonify({"response": bot_reply})

# ✅ Journaling Route
@app.route('/journaling', methods=['GET', 'POST'])
def journaling():
    # Initialize journal_entries if not already in the session
    if 'journal_entries' not in session:
        session['journal_entries'] = []

    if request.method == 'POST':
        journal_entry = request.form.get('entry')
        if journal_entry:
            # Save the journal entry to session
            session['journal_entries'].append(journal_entry)
            flash('Journal saved successfully!', 'success')  # optional flash message
            return redirect(url_for('journaling'))  # Reload the page to display new entry
    
    # Fetch journal entries from session
    journal_entries = session.get('journal_entries', [])
    return render_template('journal.html', entries=journal_entries)


# ✅ Breathing Exercise Route
@app.route('/breathing')
def breathing():
    return render_template('breathing.html')


if __name__ == '__main__':
    socketio.run(app, debug=True)
