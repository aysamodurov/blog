from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Необходима авторизация'
bootstrap = Bootstrap()
moment = Moment()


def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app,db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Необходима авторизация'
    bootstrap.init_app(app)
    moment.init_app(app)

    from app.errors import bp as bp_errors
    app.register_blueprint(bp_errors)

    from app.auth import bp as bp_auth
    app.register_blueprint(bp_auth)

    from app.main import bp as bp_main
    app.register_blueprint(bp_main)
    return app

from app import models