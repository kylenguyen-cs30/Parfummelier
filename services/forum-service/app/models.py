from mongoengine import Document, StringField, ReferenceField, ListField, DateTimeField, IntField
import datetime

# models here for user, posts, thread, comments, and messages
class User(Document):
    username = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    friends = ListField(ReferenceField('self'))
    joined_on = DateTimeField(default=datetime.datetime.utcnow)

class Post(Document):
    author = ReferenceField(User, required=True)
    title = StringField(required=True)
    content = StringField(required=True)
    rating = IntField(default=0)
    created_at = DateTimeField(default=datetime.datetime.utcnow)

class Thread(Document):
    title = StringField(required=True)
    posts = ListField(ReferenceField(Post))
    created_by = ReferenceField(User)
    created_at = DateTimeField(default=datetime.datetime.utcnow)

class Comment(Document):
    post = ReferenceField(Post, required=True)
    author = ReferenceField(User, required=True)
    content = StringField(required=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)

class Message(Document):
    sender = ReferenceField(User, required=True)
    receiver = ReferenceField(User, required=True)
    content = StringField(required=True)
    sent_at = DateTimeField(default=datetime.datetime.utcnow)
