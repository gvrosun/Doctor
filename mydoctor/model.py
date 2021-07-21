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


class Patient(db.Model):
    __tablename__ = 'patient'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    nickname = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    treatment = db.Column(db.Boolean, nullable=False)
    about_treatment = db.Column(db.String, nullable=False)
    info_choice = db.Column(db.String, nullable=False)
    others = db.Column(db.String, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, first_name, last_name, address, zip_code, phone_number, nickname, gender, date_of_birth, treatment, about_treatment, info_choice, others, patient_id):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.zip_code = zip_code
        self.phone_number = zip_code
        self.phone_number = phone_number
        self.nickname = nickname
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.treatment = treatment
        self.about_treatment = about_treatment
        self.info_choice = info_choice
        self.others = others
        self.patient_id = patient_id


class Doctor(db.Model):
    __tablename__ = 'doctor'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    nickname = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    specialization = db.Column(db.String, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    rmp_number = db.Column(db.Integer, nullable=False)
    info_choice = db.Column(db.String, nullable=False)
    others = db.Column(db.String, nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, first_name, last_name, address, zip_code, phone_number, nickname, gender, date_of_birth, specialization, rmp_number, info_choice, others, doctor_id):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.zip_code = zip_code
        self.phone_number = zip_code
        self.phone_number = phone_number
        self.nickname = nickname
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.specialization = specialization
        self.rmp_number = rmp_number
        self.info_choice = info_choice
        self.others = others
        self.doctor_id = doctor_id