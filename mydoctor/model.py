from mydoctor import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, index=True)
    username = db.Column(db.String, unique=True, index=True)
    choice = db.Column(db.String)
    password_hash = db.Column(db.String)

    def __init__(self, email, username, choice, password):
        self.email = email
        self.username = username
        self.choice = choice
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password.data)

