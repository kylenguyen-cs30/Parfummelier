from flask import Blueprint, request, jsonify
from .models import Post, Comment


forum_blueprint = Blueprint('forum', __name__)

#Create post
@forum_blueprint.route('/posts', methods=['POST'])
def create_post():
    data = request.json
    new_post = Post(
        author=data['author'],
        title=data['title'],
        content=data['content']
    )
    new_post.save()  # Save post
    return jsonify(new_post.to_json()), 201

# Fetch all posts
@forum_blueprint.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.objects()  # Fetch all posts from MongoDB
    return jsonify([post.to_json() for post in posts]), 200

#Add comment
@forum_blueprint.route('/posts/<post_id>/comment', methods=['POST'])
def add_comment(post_id):
    data = request.json
    post = Post.objects(id=post_id).first()
    if not post:
        return jsonify({"error": "Post not found"}), 404

    new_comment = Comment(
        author=data['author'],
        content=data['content']
    )
    new_comment.save()
    post.comments.append(new_comment)
    post.save()

    return jsonify(post.to_json()), 201
