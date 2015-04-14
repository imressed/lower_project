# -*- coding: utf-8 -*-
from functools import wraps
from werkzeug.security import generate_password_hash
from flask import session, g, redirect, url_for, render_template, flash, request
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from models import Post, User
from forms import PostForm, AnswerForm, RegisterForm, LoginForm


@app.before_request
def before_request():
    g.user = current_user


def not_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user.is_authenticated():
            flash('You already have an account!')
            return redirect(url_for('index', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if g.user.is_authenticated():
            return func(*args, **kwargs)
        else:
            flash('Please register first!')
            return redirect(url_for('index', next=request.url))
    return decorated_view


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if g.user.get_role() == 'admin':
            return func(*args, **kwargs)
        else:
            flash('Only admin could answer questions.')
            return redirect(url_for('index', next=request.url))
    return decorated_view


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
@app.route('/index')
def index():
    posts = reversed(Post.query.all())
    return render_template('index.html',
                           title=u'Задай питання юристу',
                           posts=posts)


@app.route('/question', methods=['GET', 'POST'])
@login_required
def question():
    form = PostForm()
    if form.validate_on_submit():
        question = Post(question=form.question.data, user_name=g.user.username)
        db.session.add(question)
        db.session.commit()
        flash('your question has successfully received! Wait for answer...')
        return redirect('/')
    return render_template('question.html',
                           title='Ask',
                           form=form)


@app.route('/answer')
#@admin_required
def answer_list():
    posts = reversed(Post.query.all())
    return render_template('answer_list.html',
                           title=u'Відповісти на запитання',
                           posts=posts)


@app.route('/answer/<int:post_id>', methods=['GET', 'POST'])
@admin_required
def answer(post_id):
    form = AnswerForm()
    post = Post.query.filter_by(id=post_id).first()
    if form.validate_on_submit():
        post.answer = form.answer.data
        db.session.commit()
        return redirect('/')
    return render_template('answer.html',
                           title=u'Відповісти на запитання',
                           post=post,
                           form=form)

@app.route('/register', methods=['GET', 'POST'])
@not_login_required
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate() and form.validate_login() == True:
        user = User(username=form.username.data, email=form.email.data,
                    password=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Thanks for registering')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    print (form.data)
    if request.method == 'POST' and form.validate() and form.validate_login() == True:
        user = form.get_user()
        login_user(user)
        flash('You are successfully login')
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are logout')
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')
