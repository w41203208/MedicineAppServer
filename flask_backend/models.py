from enum import unique
from typing import NamedTuple
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Medicine(db.Model):
    mId = db.Column(db.Integer, autoincrement=True , primary_key=True, nullable=False, )
    mName = db.Column(db.String(150), unique=True)

class Note(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    test = db.Column(db.String(100))

class MUser(db.Model):
    __tablename__ = 'M_User'

    id = db.Column(db.Integer, autoincrement=True , primary_key=True, nullable=False)
    name = db.Column(db.String(10), nullable=True)
    number = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    token = db.Column(db.String(500))

    def __init__(self, number, name, password, token):
        self.number = number
        self.name = name
        self.password = password
        self.token = token


