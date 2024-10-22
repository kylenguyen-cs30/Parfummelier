from flask import Blueprint, request, jsonify
from flask_socketio import emit, join_room, leave_room
from .models import Post, Comment
from . import socketio  # Import socketio from __init__.py

forum_blueprint = Blueprint('forum', __name__)

# Existing routes for posts and comments...

# --------------------
# WebSocket Chat Routes
# --------------------

# Handle when a user joins a chat room
@socketio.on('join')
def handle_join(data):
    username = data.get('username')
    room = data.get('room')
    if not username or not room:
        return emit('error', {'msg': 'Username and room name required'})

    join_room(room)
    emit('message', {'msg': f'{username} has joined the room.'}, room=room)

# Handle when a user leaves a chat room
@socketio.on('leave')
def handle_leave(data):
    username = data.get('username')
    room = data.get('room')
    leave_room(room)
    emit('message', {'msg': f'{username} has left the room.'}, room=room)

from datetime import datetime

# Handle sending a chat message to the room
@socketio.on('send_message')
def handle_send_message(data):
    room = data['room']
    message = data['msg']
    username = data['username']
    
    # Get the current time
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Send the message with the timestamp
    emit('message', {'msg': message, 'username': username, 'time': timestamp}, room=room)


# Handle user typing event
@socketio.on('typing')
def handle_typing(data):
    room = data['room']
    username = data['username']
    emit('typing', {'username': username}, room=room, broadcast=True)
