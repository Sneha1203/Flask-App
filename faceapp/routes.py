from importlib_metadata import files
from faceapp import app
from faceapp import db
from flask import render_template, redirect, url_for, flash, request
from faceapp.models import User, Student
from faceapp.forms import LoginUserForm, RegisterStudentForm, RegisterUserForm
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import uuid as uuid
import os 



@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/student_details', methods=['GET', 'POST'])
@login_required
def student_details():
    form = RegisterStudentForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            create_student = Student(dept=form.dept.data,
                                    course=form.course.data,
                                    year=form.year.data,
                                    semester=form.semester.data,
                                    name=form.name.data,
                                    section=form.section.data,
                                    roll_no=form.roll_no.data,
                                    gender=form.gender.data,
                                    mobile_no=form.mobile_no.data,
                                    email=form.email.data,
                                    teacher=form.teacher.data, 
                                    photo_sample=form.photo_sample.data)

            pic_filename = secure_filename(create_student.photo_sample.filename)
            pic_name = str(uuid.uuid1()) + "_" + pic_filename

            saver = request.files['photo_sample']
            saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))

            create_student.photo_sample = pic_name
            db.session.add(create_student)
            db.session.commit()
            flash(f'Student has been registered succesfully!', category='success')
            return redirect(url_for('student_details'))
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(f'There was an error with registering the student: {err_msg}',category='danger')
    if request.method == 'GET':
        students = Student.query.all()
        return render_template('student_details.html', form=form, students=students)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginUserForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Welcome {attempted_user}! You have logged in successfully!', category='success')
            return redirect(url_for('student_details'))
        else:
            flash(f'Username and password do not match! Please try again!', category='danger')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterUserForm()
    if form.validate_on_submit():
        create_user = User(username=form.username.data,
                            email=form.email.data,
                            password=form.password1.data)
        db.session.add(create_user)
        db.session.commit()
        login_user(create_user)
        flash(f'Account created successfully! You are logged in as {create_user.username}!', category='success')
        return redirect(url_for('student_details'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating user: {err_msg}', category='danger')
    return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash(f'You have logged out successfully!', category='info')
    return redirect(url_for('home'))