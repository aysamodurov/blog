from app.auth import bp
from app import db
from app.auth.forms import LoginForm, RegisterForm
from app.models import User
from flask import render_template, url_for, redirect, flash, request
from flask_login import current_user, login_user, logout_user, login_required


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
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
                return redirect(url_for('main.index'))
        else:
            flash('Неверный логин или пароль') 
            return redirect(url_for('auth.login'))
    return render_template('auth/login.html',title='Авторизация', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Регистрация', form = form)

@bp.route('/logout')
@login_required
def logout():
    if current_user:
        logout_user()
    return redirect(url_for('auth.login'))