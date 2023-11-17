from app import app, db
from app.forms import LoginForm, RegisterForm
from app.models import User
from flask import render_template, url_for, redirect, flash, request
from flask_login import current_user, login_user, logout_user, login_required


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Добро пожаловать!')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        next_page = request.args.get('next')
        print(next_page)
        user = User.query.filter_by(username = form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash("добро пожаловать {}".format(current_user.username))
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