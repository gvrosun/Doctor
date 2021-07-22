from mydoctor import app, db
from flask import render_template, redirect, request, url_for, flash, session, abort
from flask_login import login_user, login_required, logout_user, current_user
from mydoctor.model import User, Doctor, Patient
from werkzeug.utils import secure_filename
from mydoctor.forms import LoginForm, RegistrationForm, PatientProfileForm, DoctorProfileForm, Contact, Profile
import os
from datetime import timedelta


@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=15)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = Contact()
    if form.validate_on_submit():
        return redirect(url_for('index'))

    return render_template('index.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    login_success = True
    permission = False
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password) and user is not None:
            session['username'] = user.username
            session['type'] = user.choice
            if form.remember.data:
                login_user(user, remember=True)
            else:
                login_user(user)

            user_details = Patient.query.filter_by(patient_id=current_user.get_id()).first() if session['type'] == 'patient' else Doctor.query.filter_by(doctor_id=current_user.get_id()).first()
            if user_details:
                session['profile'] = True
                session['name'] = user_details.first_name
            else:
                session['profile'] = False

            return redirect(url_for('find_profile'))

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
    return redirect(url_for('index'))


@app.route('/patient_profile', methods=['GET', 'POST'])
@login_required
def patient_profile():
    if session['type'] == 'doctor':
        abort(403)
    if session['profile']:
        return redirect(url_for('patient'))
    else:
        form = PatientProfileForm()
        if form.validate_on_submit():
            patient_details = Patient(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                address=form.address.data,
                zip_code=form.zip_code.data,
                phone_number=form.phone_number.data,
                nickname=form.nickname.data,
                gender=form.gender.data,
                date_of_birth=form.date_of_birth.data,
                treatment=form.treatment.data,
                about_treatment=form.about_treatment.data,
                info_choice=form.info_choice.data,
                others=form.others.data,
                patient_id=current_user.get_id()
            )
            db.session.add(patient_details)
            db.session.commit()
            session['name'] = form.first_name
            return redirect(url_for('patient'))

        return render_template('PatientProfile.html', form=form)


@app.route('/doctor_profile', methods=['GET', 'POST'])
@login_required
def doctor_profile():
    if session['type'] == 'patient':
        abort(403)
    if session['profile']:
        return redirect(url_for('doctor'))
    else:
        doctor_account_details = User.query.filter_by(id=current_user.get_id()).first()
        form = DoctorProfileForm()
        if form.validate_on_submit():
            doctor_details = Doctor(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                address=form.address.data,
                zip_code=form.zip_code.data,
                phone_number=form.phone_number.data,
                nickname=form.nickname.data,
                gender=form.gender.data,
                date_of_birth=form.date_of_birth.data,
                specialization=form.specialization.data,
                rmp_number=form.rmp_number.data,
                info_choice=form.info_choice.data,
                others=form.others.data,
                doctor_id=current_user.get_id()
            )
            if form.certificate_file.data:
                filename = secure_filename(form.certificate_file.data.filename)
                extension = filename.split('.')[-1]
                form.certificate_file.data.save(os.path.join(app.config['UPLOAD_FOLDER'], f'{doctor_account_details.username}.{extension}'))
            db.session.add(doctor_details)
            db.session.commit()
            return redirect(url_for('doctor'))

        return render_template('DoctorProfile.html', form=form)


@app.route('/patient')
@login_required
def patient():
    if session['type'] == 'doctor':
        abort(403)

    return render_template('Patient.html', name=session['name'])


@app.route('/doctor')
@login_required
def doctor():
    if session['type'] == 'patient':
        abort(403)
    return render_template('Doctor.html', name=session['name'])


@app.route('/find_profile')
@login_required
def find_profile():
    if session['type'] == 'doctor':
        if session['profile']:
            return redirect(url_for('doctor'))
        else:
            return redirect(url_for('doctor_profile'))
    elif session['type'] == 'patient':
        if session['profile']:
            return redirect(url_for('patient'))
        else:
            return redirect(url_for('patient_profile'))


@app.route('/profile/<name>', methods=['GET', 'POST'])
@login_required
def profile(name):
    user_details = Patient.query.filter_by(patient_id=current_user.get_id()).first() if session['type'] == 'patient' else Doctor.query.filter_by(doctor_id=current_user.get_id()).first()
    form = Profile()
    form.first_name.data = user_details.first_name
    form.last_name.data = user_details.last_name
    form.location.data = user_details.address
    if form.validate_on_submit():
        pass
    return render_template('Profile.html', form=form)


@app.route('/check')
@login_required
def check():
    return redirect(f"/profile/{session['username']}")


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


@app.route('/error')
def error():
    return render_template('502.html'), 502


@app.errorhandler(403)
def permission_denied(e):
    return render_template('403.html'), 403


if __name__ == '__main__':
    app.run(debug=True)
