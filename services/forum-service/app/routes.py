from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Category, Topic, Post, db

app = Flask(__name__)

@app.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    category_list = [{"id": c.id, "name": c.name, "description": c.description} for c in categories]
    return jsonify(category_list), 200

@app.route('/category/<int:category_id>/topics', methods=['GET'])
def get_topics_in_category(category_id):
    topics = Topic.query.filter_by(category_id=category_id).all()
    topic_list = [{"id": t.id, "title": t.title, "created_at": t.created_at} for t in topics]
    return jsonify(topic_list), 200

@app.route('/category/<int:category_id>/new-topic', methods=['POST'])
def create_topic(category_id):
    data = request.get_json()
    new_topic = Topic(title=data['title'], user_id=data['user_id'], category_id=category_id)
    db.session.add(new_topic)
    db.session.commit()
    return jsonify({"message": "Topic created successfully"}), 201

@app.route('/topic/<int:topic_id>/posts', methods=['GET'])
def get_posts_in_topic(topic_id):
    posts = Post.query.filter_by(topic_id=topic_id).all()
    post_list = [{"id": p.id, "content": p.content, "author": p.author.username, "created_at": p.created_at} for p in posts]
    return jsonify(post_list), 200

@app.route('/topic/<int:topic_id>/new-post', methods=['POST'])
def create_post(topic_id):
    data = request.get_json()
    new_post = Post(content=data['content'], user_id=data['user_id'], topic_id=topic_id)
    db.session.add(new_post)
    db.session.commit()
    return jsonify({"message": "Post created successfully"}), 201
