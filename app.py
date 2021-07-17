from mydoctor import app, db
from flask import render_template, redirect, request, url_for
from flask_login import login_user, login_required, logout_user
from mydoctor.model import User
from mydoctor.forms import LoginForm, RegistrationForm, PatientProfileForm, DoctorProfileForm


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password) and user is not None:
            login_user(user)
            next_page = request.args.get('next')
            if next_page is None or not next_page[0] == '/':
                if user.choice == 'patient':
                    next_page = url_for('patient')
                elif user.choice == 'doctor':
                    next_page = url_for('doctor')

            print(next_page)
            return redirect(next_page)
        return redirect(url_for('patient_profile'))

    valid = False
    if request.args.get('next') is not None:
        valid = True
    return render_template('Login.html', form=form, valid=valid)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data,
            choice=form.choice.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('SignUp.html', form=form)


@app.route('/logout')
@login_required
def logout():
    return render_template('index.html')


@app.route('/patient_profile', methods=['GET', 'POST'])
@login_required
def patient_profile():
    form = PatientProfileForm()
    if form.validate_on_submit():
        return redirect(url_for('patient'))

    return render_template('PatientProfile.html', form=form)


@app.route('/patient')
def patient():
    return render_template('Patient.html')


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


if __name__ == '__main__':
    app.run(debug=True)
