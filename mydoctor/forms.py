from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField, RadioField, BooleanField, TextAreaField, SelectField, \
    FileField, EmailField, DateField, TelField
from wtforms.validators import DataRequired, EqualTo, Length, regexp
from mydoctor.model import User


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Length(min=5, max=35)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), ])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('New Password', [
        DataRequired(),
        EqualTo('confirm')
    ])
    confirm = PasswordField('Repeat Password', validators=[DataRequired()])
    choice = SelectField(u'WHO YOU ARE', choices=[(None, '-select-'), ('patient', 'Patient'), ('doctor', 'Doctor')],
                         default=None)
    submit = SubmitField('Register')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            return False
        return True

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            return False
        return True


class PatientProfileForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    zip_code = StringField('Zip code', validators=[DataRequired()])
    phone_number = TelField('Phone number', validators=[DataRequired()])
    nickname = StringField('Nickname', validators=[DataRequired()])
    gender = RadioField('Gender', choices=[('male', 'Male'), ('female', 'Female')], default='male')
    date_of_birth = DateField('Date of Birth: ', validators=[DataRequired()])
    treatment = BooleanField('Have you take any treatment before?')
    about_treatment = TextAreaField('If Checked', render_kw={'rows': 4, 'cols': 50}, validators=[DataRequired()])
    info_choice = RadioField('How do you know about this Application?',
                             choices=[('family', 'By family/friends'), ('social', 'By social media'),
                                      ('others', 'Others')])
    others = StringField('If others')
    submit = SubmitField('Submit')


class DoctorProfileForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    zip_code = StringField('Zip code', validators=[DataRequired()])
    phone_number = TelField('Phone number', validators=[DataRequired()])
    nickname = StringField('Nickname', validators=[DataRequired()])
    gender = RadioField('Gender', choices=[('male', 'Male'), ('female', 'Female')], default='male')
    specialization = StringField('Specialization', validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth: ', validators=[DataRequired()])
    rmp_number = StringField('RMP Number', validators=[DataRequired()])
    certificate_file = FileField('Upload your RPM Certificate', validators=[DataRequired()])
    info_choice = RadioField('How do you know about this Application?',
                             choices=[('family', 'By family/friends'), ('social', 'By social media'),
                                      ('others', 'Others')])
    others = StringField('If others')
    submit = SubmitField('Submit')
