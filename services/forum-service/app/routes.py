# routes.py

from flask import Blueprint, request, jsonify
from .models import User, Post, Thread, Comment, Message

forum_blueprint = Blueprint('forum_blueprint', __name__)

# Routes for forum services

# Messaging route
@forum_blueprint.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    try:
        sender = User.objects.get(id=data['sender_id'])
        receiver = User.objects.get(id=data['receiver_id'])
        message = Message(sender=sender, receiver=receiver, content=data['content'])
        message.save()
        return jsonify({"message": "Message sent successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Update relationship (add/remove friends)
@forum_blueprint.route('/update_relationship', methods=['POST'])
def update_relationship():
    data = request.json
    try:
        user1 = User.objects.get(id=data['user1_id'])
        user2 = User.objects.get(id=data['user2_id'])
        if data['action'] == 'add_friend':
            user1.friends.append(user2)
            user2.friends.append(user1)
        elif data['action'] == 'remove_friend':
            user1.friends.remove(user2)
            user2.friends.remove(user1)
        user1.save()
        user2.save()
        return jsonify({"message": "Relationship status updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# for returning friend list
@forum_blueprint.route('/friends/<user_id>', methods=['GET'])
def get_friends(user_id):
    try:
        user = User.objects.get(id=user_id)
        friends = [{"username": friend.username, "email": friend.email} for friend in user.friends]
        return jsonify(friends), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# rating post function
@forum_blueprint.route('/rate_post', methods=['POST'])
def rate_post():
    data = request.json
    try:
        post = Post.objects.get(id=data['post_id'])
        post.rating += data['rating']
        post.save()
        return jsonify({"message": "Post rating updated!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# create thread/post
@forum_blueprint.route('/create_thread', methods=['POST'])
def create_thread():
    data = request.json
    try:
        user = User.objects.get(id=data['user_id'])
        thread = Thread(title=data['title'], created_by=user)
        thread.save()
        return jsonify({"message": "Thread created successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# add comment to post
@forum_blueprint.route('/add_comment', methods=['POST'])
def add_comment():
    data = request.json
    try:
        user = User.objects.get(id=data['user_id'])
        post = Post.objects.get(id=data['post_id'])
        comment = Comment(author=user, post=post, content=data['content'])
        comment.save()
        return jsonify({"message": "Comment added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# return posts in thread
@forum_blueprint.route('/related_posts/<thread_id>', methods=['GET'])
def get_related_posts(thread_id):
    try:
        thread = Thread.objects.get(id=thread_id)
        related_posts = [{"title": post.title, "content": post.content, "author": post.author.username} for post in thread.posts]
        return jsonify(related_posts), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
