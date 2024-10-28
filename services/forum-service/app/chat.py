# chat.py
from flask import Blueprint, request, jsonify
from flask_socketio import join_room, leave_room, emit
from app.db import chatrooms_collection, messages_collection

# Initialize the chat blueprint
chat_blueprint = Blueprint("chat", __name__)

# HTTP Route to check if the chat service is online
@chat_blueprint.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Chat service is online"})

# HTTP Route to create a new chatroom
@chat_blueprint.route("/chatroom", methods=["POST"])
def create_chatroom():
    data = request.json
    participants = data.get("participants")
    if not participants:
        return jsonify({"error": "Participants are required"}), 400

    chatroom = {
        "participants": participants
    }
    result = chatrooms_collection.insert_one(chatroom)
    return jsonify({"chatroom_id": str(result.inserted_id)}), 201

# This function will register the socket.io events
def register_socketio_events(socketio):
    
    @socketio.on("join")
    def handle_join(data):
        chatroom_id = data["chatroomId"]
        join_room(chatroom_id)
        emit("message", {"msg": "User joined the room"}, room=chatroom_id)

    @socketio.on("send_message")
    def handle_send_message(data):
        chatroom_id = data["chatroomId"]
        message = {
            "chatroom_id": chatroom_id,
            "user_id": data["userId"],
            "message": data["messageContent"],
            "timestamp": data["timestamp"]
        }
        messages_collection.insert_one(message)
        emit("new_message", message, room=chatroom_id)

    @socketio.on("leave")
    def handle_leave(data):
        chatroom_id = data["chatroomId"]
        leave_room(chatroom_id)
        emit("message", {"msg": f"User {data['userId']} has left the chatroom"}, room=chatroom_id)
