
from mongoengine import Document, StringField, ListField, ReferenceField, DateTimeField
from datetime import datetime

#For commenting
class Comment(Document):
    author = StringField(required=True)
    content = StringField(required=True)
    timestamp = DateTimeField(default=datetime.utcnow)

#For posting
class Post(Document):
    author = StringField(required=True)
    title = StringField(required=True)
    content = StringField(required=True)
    comments = ListField(ReferenceField(Comment))
    timestamp = DateTimeField(default=datetime.utcnow)
