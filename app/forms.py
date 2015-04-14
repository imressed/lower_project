# -*- coding: utf-8 -*-
__author__ = 'imressed'

from flask import url_for, flash, redirect
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, TextField
from wtforms.validators import Required, EqualTo, ValidationError
from app import db
from models import User
from werkzeug.security import check_password_hash


class PostForm(Form):
    question = StringField ('question', [Required()])


class AnswerForm(Form):
    answer = StringField ('question', [Required()])

class RegisterForm(Form):
    username = StringField('Username', [Required()])
    email = StringField('email', [Required()])
    password = PasswordField('password', [
        Required(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [Required()])

    def validate_login(self):
        if User.query.filter_by(username=self.username.data).count() > 0:
            flash('This login is alerady used! Try other')
            return redirect(url_for('register'))
        return True

class LoginForm(Form):
    username = TextField('Username', [Required()])
    password = PasswordField('Password', [Required()])

    def validate_login(self):
        user = self.get_user()

        if user is None:
            flash('There is no user with such username')
            return redirect(url_for('login'))

        if not check_password_hash(user.password, self.password.data):
            flash('Password is incorect, try other')
            return redirect(url_for('login'))
        return True

    def get_user(self):
        return User.query.filter_by(username=self.username.data).first()



