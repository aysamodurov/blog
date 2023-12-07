from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app,db)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Необходима авторизация'
bootstrap = Bootstrap(app)
moment = Moment(app)

from app.errors import bp as bp_errors
app.register_blueprint(bp_errors)

from app.auth import bp as bp_auth
app.register_blueprint(bp_auth)

from app.main import bp as bp_main
app.register_blueprint(bp_main)


from app import models