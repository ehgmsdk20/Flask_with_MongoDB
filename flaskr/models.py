
from flask_mongoengine.wtf import model_form
from flask_mongoengine import MongoEngine
import mongoengine
from wtforms import validators

from flask_login import UserMixin
from bson.objectid import ObjectId

import datetime

db = MongoEngine()

class User(db.Document, UserMixin):
    user_id = db.StringField(primary_key=True, validators=[validators.InputRequired(message='Missing ID.'),])
    password = db.StringField(required=True, min_length = 7)

class Post(db.Document):
    title = db.StringField(max_length=120, required=True, validators=[validators.InputRequired(message='Missing title.'),])
    body = db.StringField(max_length=120, required=True, validators=[validators.InputRequired(message='Missing content.'),])
    created =  db.DateTimeField(default=datetime.datetime.utcnow() + datetime.timedelta(hours=9))
    author = db.ReferenceField(User, dbref=True, reverse_delete_rule = 2) #CASCADE=2
    @classmethod
    def find(cls, id):
        return cls.objects(id=ObjectId(id)).first()

