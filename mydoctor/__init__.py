import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail

login_manager = LoginManager()
basedir = os.path.dirname(__file__)
app = Flask(__name__)
app.config['SECRET_KEY'] = "key_for_doctor_project"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), './uploads/')

db = SQLAlchemy(app)
Migrate(app, db)
mail = Mail(app)

login_manager.init_app(app)
login_manager.login_view = 'auth'
login_manager.refresh_view = 'auth'
login_manager.needs_refresh_message = "Session timeout, please re-login"
login_manager.needs_refresh_message_category = "info"