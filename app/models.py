from app import db, login_manager
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email= db.Column(db.String, unique=True, nullable=False)
    last_seen =db.Column(db.DateTime,default=datetime.utcnow)
    about_me = db.Column(db.String)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<User: {} , email: {}>".format(self.username, self.email)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
