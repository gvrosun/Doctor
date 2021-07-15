from flask import Flask, render_template
from flask_login import login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = "key"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print(email, password)

    return render_template('Login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('SignUp.html')


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


if __name__ == '__main__':
    app.run(debug=True)
