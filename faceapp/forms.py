from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, IntegerField, SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from faceapp.models import User, Student



class LoginUserForm(FlaskForm):
    username = StringField(label='Username: ', validators=[DataRequired()])
    password = PasswordField(label='Password: ', validators=[DataRequired()])
    submit = SubmitField(label='Sign In: ')



class RegisterUserForm(FlaskForm):

    def validate_username(self, username_to_Check):
        user = User.query.filter_by(username=username_to_Check.data).first()
        if user:
            raise ValidationError('Username Already Exists! Try Different Username!')

    def validate_email(self, email_to_check):
        email = User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('Email Aready Exists! Try different Email!')

    username = StringField(label='Username: ', validators=[Length(min=2, max=10), DataRequired()])
    email = StringField(label='Email Address: ', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password: ', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password: ', validators=[EqualTo(password1), DataRequired()])
    submit = SubmitField(label='Create Account')



class RegisterStudentForm(FlaskForm):

    def validate_email(self, email_to_check):
        email = User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('Email Aready Exists! Try different Email!')

    dept = SelectField(label='Department: ', validators=[DataRequired()])
    course = SelectField(label='Course: ', validators=[DataRequired()])
    year = SelectField(label='Year: ', validators=[DataRequired()])
    semester = SelectField(label='Semester: ', validators=[DataRequired()])
    name = StringField(label='Student Name: ', validators=[DataRequired()])
    section = SelectField(label='Section: ', validators=[DataRequired()])
    roll_no = IntegerField(label='Roll Number: ', validators=[DataRequired()])
    gender = SelectField(label='Gender: ', validators=[DataRequired()])
    mobile_no = StringField(label='Mobile Number: ', validators=[DataRequired()])
    email = StringField(label='Email Address: ', validators=[DataRequired()])
    teacher = StringField(label='Teacher: ', validators=[DataRequired()])
    photo_sample = FileField(label='Upload a Photo: ', validators=[DataRequired()])

    

