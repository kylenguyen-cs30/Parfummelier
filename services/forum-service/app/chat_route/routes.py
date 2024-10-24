from flask import Blueprint, request, jsonify
from flask_socketio import join_room, leave_room, emit
from app.socketio import socketio

# from app import socketio
from app.chat_route.models import (
    add_message,
    get_messages,
    create_chatroom,
    get_chatroom,
)


# Function to initialize socketio
def init_socketio(sio):
    global socketio
    socketio = sio


# Create a chat blueprint
chat_blueprint = Blueprint("chat", __name__)


@chat_blueprint.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Chat service is online"})


# NOTE: HTTPE Route to create a new chatroom
@chat_blueprint.route("/chatroom", methods=["POST"])
def create_new_chatroom():
    data = request.json
    participants = data.get("participants")
    if not participants:
        return jsonify({"error": "participants are required"}), 400

    chatroom_id = create_chatroom(participants)
    return jsonify({"chatroom": chatroom_id}), 201


# NOTE: HTTP route to get messages from a chatroom
@chat_blueprint.route("/chatroom/<chatroom_id>/messages", methods=["GET"])
def get_chatroom_messages(chatroom_id):
    messages = get_messages(chatroom_id)
    if not messages:
        return jsonify({"error": "No messages found"}), 404
    return jsonify(messages), 200


# NOTE: Connect
@socketio.on("connect")
def handle_connect():
    print("Client connected")
    emit("connection_response", {"data": "Connected"})


# NOTE: disconnect
@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")


# NOTE: WebSocket route to join a chatroom
@socketio.on("join")
def handle_join(data):
    chatroom_id = data["chatroomId"]
    join_room(chatroom_id)
    emit(
        "message",
        {"msg": f"User {data['userId']} has joined the chatroom"},
        room=chatroom_id,
    )


# NOTE: WebSocket route to send a message
@socketio.on("send_message")
def handle_message(data):
    chatroom_id = data["chatroomId"]
    sender_id = data["userId"]
    message_content = data["messageContent"]

    # Add the message to the database
    message = add_message(chatroom_id, sender_id, message_content)

    # Broadcast the message to all users in the chatroom
    emit("new_message", message, room=chatroom_id)


# NOTE: WebSocket route to leave a chatroom
@socketio.on("leave")
def handle_leave(data):
    chatroom_id = data["chatroomId"]
    leave_room(chatroom_id)
    emit(
        "message",
        {"msg": f"User {data['userId']} has left the chatroom"},
        room=chatroom_id,
    )
