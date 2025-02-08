from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'  # Replace with a strong secret key
socketio = SocketIO(app)

# Dictionary to track active rooms
rooms = {}

@app.route('/')
def home():
    return render_template('index.html')

@socketio.on('join_room')
def handle_join(data):
    username = data['username']
    room = data['room']
    join_room(room)

    # Add user to the room's active list
    if room not in rooms:
        rooms[room] = []
    rooms[room].append(username)

    # Notify the room about the new user
    emit('message', {'username': 'System', 'message': f"{username} has joined the room."}, to=room)

@socketio.on('leave_room')
def handle_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)

    # Remove user from the room's active list
    if room in rooms and username in rooms[room]:
        rooms[room].remove(username)

    # Notify the room about the user leaving
    emit('message', {'username': 'System', 'message': f"{username} has left the room."}, to=room)

@socketio.on('send_message')
def handle_message(data):
    username = data['username']
    room = data['room']
    message = data['message']

    # Broadcast the message to the room
    emit('message', {'username': username, 'message': message}, to=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)
