import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///'+os.path.join(basedir,"blog.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 2