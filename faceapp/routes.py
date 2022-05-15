from numpy import save
from faceapp import app
from faceapp import db
from flask import render_template, redirect, url_for, flash, request, Response
from faceapp.models import User, Student
from faceapp.forms import LoginUserForm, RegisterStudentForm, RegisterUserForm
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import uuid as uuid
from datetime import datetime
import os 
import cv2
from PIL import Image
import numpy as np

camera = cv2.VideoCapture(0)

def attendance(self, id, roll_no, name):
        with open('attendance.csv', 'r+', newline='\n') as file:
            data_list = file.readlines()
            name_list = []
            for line in data_list:
                entry = line.split((','))
                name_list.append(entry[0])

            if((id not in name_list) and (roll_no not in name_list) and (name not in name_list)):
                now = datetime.now()
                date_str = now.strftime ('%d/%m/%Y')
                time_str = now.strftime('%H:%M:%S')
                file.writelines(f'\n{id}, {roll_no}, {name}, {time_str}, {date_str}, Present')

def gen_frames():
    while True:
        success, frame=camera.read()
        if not success:
            break
        else:
            def draw_box(image, classifier, scale_factor, min_neighbour, color, text, trained_classifier):
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                descriptors = classifier.detectMultiScale(gray_image, scale_factor, min_neighbour)

                coordinates = []

                for (x, y, w, h) in descriptors:
                    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    id, predict = trained_classifier.predict(gray_image[y:y+h, x:x+w])
                    confidence = int((100 * (1-predict / 300)))

                    result = Student.query.filter_by(id=id)
     
                    if result is not None:
                        student_name = result.name

                    # my_cursor.execute('select * from student where student_id=' + str(id))
                    # roll = my_cursor.fetchone()
                        roll_no = result.roll_no

                    # my_cursor.execute('select * from student where student_id=' + str(id))
                    # s_id = my_cursor.fetchone()
                        student_id = result.id

                        if confidence > 80:
                            cv2.putText(image, f'ID: {student_id}', (x, y-55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 1)
                            cv2.putText(image, f'Roll No.: {roll_no}', (x, y-30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 1)
                            cv2.putText(image, f'Name: {student_name}', (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 1)
                            attendance(student_id, roll_no, student_name)
                    else:
                        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 1)
                        cv2.putText(image, 'Unknown Face', (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 1)

                    coordinates = [x, y, w, h]
                return coordinates


            def recognizer(image, trained_classifier, face_cascade):
                coordinates = draw_box(image, face_cascade, 1.1, 10, (255, 25, 255), 'Face', trained_classifier)
                return image
                        

            face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            trained_classifier = cv2.face.LBPHFaceRecognizer_create()
            trained_classifier.read('classifier.xml')

        
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = recognizer(frame, trained_classifier, face_cascade)
            frame = buffer.tobytes()
        
            yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            if cv2.waitKey(1) == 13:
                break

        camera.release()
        cv2.destroyAllWindows()

            


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


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
            
            faces = []
            ids = []
            img = Image.open(saver).convert('L')
            img_np = np.array(img, dtype='uint8')
            faces.append(img_np)
  
            id = create_student.id
            ids.append(id)
            id_np = np.array(ids)
            ids = [0] * len(faces)
            classifier = cv2.face.LBPHFaceRecognizer_create()
            classifier.train(faces, np.array(ids))
            classifier.write('classifier.xml')
            cv2.destroyAllWindows()
            flash(f'Data Set Trained Successfully!', category='success')

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
            return redirect(url_for('profile'))
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
        return redirect(url_for('profile'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating user: {err_msg}', category='danger')
    return render_template('register.html', form=form)



@app.route('/attendance_details')
def attendance_details():
    return render_template('attendance_details.html')



@app.route('/take_attendance')
def take_attendance():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/logout')
def logout():
    logout_user()
    flash(f'You have logged out successfully!', category='info')
    return redirect(url_for('home'))


