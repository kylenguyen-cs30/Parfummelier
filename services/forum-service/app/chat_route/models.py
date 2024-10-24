from bson.objectid import ObjectId
from datetime import datetime
from app import chatrooms_collection, messages_collection


# NOTE: create a chatroom
def create_chatroom(participants):
    chatroom = {"participants": participants, "createAt": datetime.now()}
    # insert into MongoDB
    result = chatrooms_collection.insert_one(chatroom)
    return str(result.inserted_id)


# NOTE: Get Chatroom by ID
def get_chatroom(chatroom_id):
    return chatrooms_collection.find_one({"_id": Objectid(chatroom_id)})


# NOTE: add a message to a chatroom
def add_message(chatroom_id, sender_id, message_content):
    message = {
        "chatroomId": chatroom_id,
        "senderId": sender_id,
        "messageContent": message_content,
        "sentAt": datetime.now(),
    }
    messages_collection.insert_one(message)
    return message


# NOTE: Function to get messages from a chatroom
def get_messages(chatroom_id):
    # Retrieve all messages associated with a specific chatroom
    messages = messages_collection.find({"chatroomId": chatroom_id}).sort("sentAt", 1)
    return list(messages)  # Convert to a list for easier handling
