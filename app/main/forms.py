from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length
from app.models import User


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


class AddPostForm(FlaskForm):
    body = TextAreaField('Сообщение', validators=[Length(min=0, max=200)])
    submit = SubmitField('Опубликовать')
