from app import app, db
from app.models import User

@app.make_shell_context
def make_shell_context():
    return {'app': app, 'db': db, 'User': User}