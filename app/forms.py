from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError, Length
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class RegisterForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    repassword = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Зарегистироваться')
    
    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Имя пользовтеля {} уже занято'.format(username.data))
    
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email {} уже занят'.format(email.data))

class EditForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    about_me = TextAreaField('Обо мне', validators=[Length(min=0, max=200)])
    submit = SubmitField('Редактировать')

    def __init__(self, original_username, *args, **kwargs):
        super(EditForm, self).__init__(*args,**kwargs)
        self.original_username = original_username
    
    def validate_username(self,username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None or username:
                raise ValidationError('Имя пользовтеля {} уже занято'.format(username.data))
