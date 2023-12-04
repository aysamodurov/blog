from app import app, db
from app.forms import LoginForm, RegisterForm, EditForm, AddPostForm
from app.models import User, Post
from flask import render_template, url_for, redirect, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = current_user.followed_posts()
    followed_users = current_user.followed.all()
    

    return render_template('index.html', title='Добро пожаловать!', followed_users = followed_users, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        next_page = request.args.get('next')
        user = User.query.filter_by(username = form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash("Добро пожаловать {}".format(current_user.username))
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('index'))
        else:
            flash('Неверный логин или пароль') 
            return redirect(url_for('login'))
    return render_template('login.html',title='Авторизация', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form = form)

@app.route('/logout')
def logout():
    if current_user:
        logout_user()
    return redirect(url_for('login'))

@app.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()
    posts = user.posts
    if user is not None:
        return render_template('profile.html', user=user, posts=posts)
    else:
        flash('Пользователь {} не найден'.format(username))

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Информация обновлена')
        return redirect(url_for('profile', username=current_user.username))
    form.username.data = current_user.username
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Редактирование информации', form=form)

@app.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = AddPostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data, body = form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('profile', username=current_user.username))
    return render_template('new_post.html', title='Новый пост', form=form)        

@app.route('/delete_post/<id>')
@login_required
def delete_post(id):
    post = Post.query.get(int(id))
    print(post.author)
    print(current_user)
    print(post.author is current_user)
    if post.author is current_user:
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('profile', username=current_user.username))

@app.route('/follow/<id>')
def follow(id):
    user = User.query.get(int(id))
    current_user.follow(user)
    db.session.commit()
    return redirect(url_for('profile', username=user.username))

@app.route('/unfollow/<id>')
def unfollow(id):
    user = User.query.get(int(id))
    current_user.unfollow(user)
    db.session.commit()
    return redirect(url_for('profile', username=user.username))

@app.route('/explore')
def explore():
    posts = Post.query.order_by(Post.dt.desc()).all()
    return render_template('index.html', title='Все посты', posts=posts)