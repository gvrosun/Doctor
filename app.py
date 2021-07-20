from mydoctor import app, db
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from mydoctor.model import User
from werkzeug.utils import secure_filename
from mydoctor.forms import LoginForm, RegistrationForm, PatientProfileForm, DoctorProfileForm
import os


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    login_success = True
    permission = False
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password) and user is not None:
            login_user(user)
            next_page = '/error'
            if user.choice == 'patient':
                next_page = url_for('patient_profile')
            elif user.choice == 'doctor':
                next_page = url_for('doctor_profile')

            return redirect(next_page)
        else:
            login_success = False
            return render_template('Login.html', form=form, permission=permission, login_success=login_success)

    if request.args.get('next') is not None:
        permission = True
    return render_template('Login.html', form=form, permission=permission, login_success=login_success)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        check_username = form.check_username(form.username)
        check_email = form.check_email(form.email)
        if check_username and check_email:
            user = User(
                email=form.email.data,
                username=form.username.data,
                choice=form.choice.data,
                password=form.password.data
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            if not check_username:
                flash('username')
            if not check_email:
                flash('email')

    return render_template('SignUp.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('index.html')


@app.route('/patient_profile', methods=['GET', 'POST'])
@login_required
def patient_profile():
    form = PatientProfileForm()
    if form.validate_on_submit():
        return redirect(url_for('patient'))

    return render_template('PatientProfile.html', form=form)


@app.route('/doctor_profile', methods=['GET', 'POST'])
@login_required
def doctor_profile():
    form = DoctorProfileForm()
    if form.validate_on_submit():
        if form.certificate_file.data:
            filename = secure_filename(form.certificate_file.data.filename)
            form.certificate_file.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return render_template('DoctorProfile.html', form=form)


@app.route('/patient')
def patient():
    return render_template('Patient.html')


@app.route('/profile/<name>')
@login_required
def profile(name):
    return render_template('Profile.html', name=name)


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


@app.route('/error')
def error():
    return "Something went wrong", 502


if __name__ == '__main__':
    app.run(debug=True)
