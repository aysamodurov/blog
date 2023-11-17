from app import app, db
from flask import render_template

@app.errorhandler(500)
def database_error(error):
    db.session.rollback()
    return render_template("500.html", title='Ошибка'), 500

@app.errorhandler(404)
def database_error(error):
    return render_template("404.html", title='Страница не найдена'), 404