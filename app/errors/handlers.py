from app import db
from app.errors import bp
from flask import render_template

@bp.app_errorhandler(500)
def database_error(error):
    db.session.rollback()
    return render_template("errors/500.html", title='Ошибка'), 500

@bp.app_errorhandler(404)
def database_error(error):
    return render_template("errors/404.html", title='Страница не найдена'), 404