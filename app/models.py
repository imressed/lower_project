# -*- coding: utf-8 -*-
__author__ = 'imressed'

from app import db
from datetime import datetime

class Post(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_name = db.Column(db.String(1024))
    question = db.Column(db.String(1024))
    time = db.Column(db.DateTime)
    answer = db.Column(db.String(1024))


    def __init__(self, question, user_id=0, user_name='Anonumys'):
        self.question = question
        self.time = datetime.now()
        self.user_id = user_id
        self.user_name = user_name


    def __repr__(self):
        return '<User %r>' % self.id

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(120), index=True)
    role = db.Column(db.String(120), index=True)
    questions = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, username, email, password, role='user'):
        self.username = username
        self.email = email
        self.password = password
        self.role = role

    def is_authenticated(self):
        return True

    def get_role(self):
        return self.role

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)

