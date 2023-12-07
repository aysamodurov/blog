from app import db
from app.main.forms import  EditForm, AddPostForm
from app.models import User, Post
from app.main import bp
from flask import render_template, url_for, redirect, flash, request, current_app
from flask_login import current_user, login_required
from datetime import datetime


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = AddPostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))

    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False
    )
    prev_url = url_for('main.index', page=posts.prev_num) if posts.has_prev else None
    next_url = url_for('main.index', page=posts.next_num) if posts.has_next else None

    followed_users = current_user.followed.all()
    return render_template('main/index.html', title='Добро пожаловать!', posts=posts.items,
                             form=form, prev_url=prev_url, next_url=next_url)

@bp.route('/explore')
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.dt.desc()).paginate(
        page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    prev_url = url_for('main.explore', page = posts.prev_num) if posts.has_prev else None
    next_url = url_for('main.explore', page = posts.next_num) if posts.has_next else None
    return render_template('main/index.html', title='Все посты', posts=posts.items, 
                            prev_url=prev_url, next_url=next_url)

@bp.route('/profile/<username>')
@login_required
def profile(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first()
    followers = user.follower.all()
    posts = user.posts.order_by(Post.dt.desc()).paginate(
        page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False
    )
    prev_url = url_for('main.profile',username=username, page=posts.prev_num) if posts.has_prev else None
    next_url = url_for('main.profile', username=username, page=posts.next_num) if posts.has_next else None
    if user is not None:
        return render_template('main/profile.html', user=user, followers=followers,
                                 posts=posts, prev_url=prev_url, next_url=next_url)
    else:
        flash('Пользователь {} не найден'.format(username))

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Информация обновлена')
        return redirect(url_for('main.profile', username=current_user.username))
    form.username.data = current_user.username
    form.about_me.data = current_user.about_me
    return render_template('main/edit_profile.html', title='Редактирование информации', form=form)

@bp.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = AddPostForm()
    if form.validate_on_submit():
        post = Post(body = form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.profile', username=current_user.username))
    return render_template('main/new_post.html', title='Новый пост', form=form)        

@bp.route('/delete_post/<id>')
@login_required
def delete_post(id):
    post = Post.query.get(int(id))
    if post.author == current_user:
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('main.profile', username=current_user.username))

@bp.route('/follow/<id>')
def follow(id):
    user = User.query.get(int(id))
    current_user.follow(user)
    db.session.commit()
    return redirect(url_for('main.profile', username=user.username))

@bp.route('/unfollow/<id>')
def unfollow(id):
    user = User.query.get(int(id))
    current_user.unfollow(user)
    db.session.commit()
    return redirect(url_for('main.profile', username=user.username))
