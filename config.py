# -*- coding: utf-8 -*-
__author__ = 'imressed'
import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

WTF_CSRF_ENABLED = True
SECRET_KEY = '58%q#n=u6^zmv%b-77)yp29x^kgxvla&^j%aat^vp5burhf+&8'
HOST='127.0.0.1'

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},

]

