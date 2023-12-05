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

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = AddPostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))

    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False
    )
    prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None
    next_url = url_for('index', page=posts.next_num) if posts.has_next else None

    followed_users = current_user.followed.all()
    return render_template('index.html', title='Добро пожаловать!', posts=posts.items,
                             form=form, prev_url=prev_url, next_url=next_url)

@app.route('/explore')
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.dt.desc()).paginate(
        page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    prev_url = url_for('explore', page = posts.prev_num) if posts.has_prev else None
    next_url = url_for('explore', page = posts.next_num) if posts.has_next else None
    return render_template('index.html', title='Все посты', posts=posts.items, 
                            prev_url=prev_url, next_url=next_url)

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
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first()
    followers = user.follower.all()
    posts = user.posts.order_by(Post.dt.desc()).paginate(
        page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False
    )
    prev_url = url_for('profile',username=username, page=posts.prev_num) if posts.has_prev else None
    next_url = url_for('profile', username=username, page=posts.next_num) if posts.has_next else None
    if user is not None:
        return render_template('profile.html', user=user, followers=followers,
                                 posts=posts, prev_url=prev_url, next_url=next_url)
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
        post = Post(body = form.body.data, author=current_user)
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
