
from flask_mongoengine.wtf import model_form
from flask_mongoengine import MongoEngine

from flask_login import UserMixin

db = MongoEngine()

class User(db.Document, UserMixin):
    username = db.StringField(primary_key=True)
    password = db.StringField(required=True)

