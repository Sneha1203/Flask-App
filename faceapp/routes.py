from faceapp import app
from flask import render_template, redirect, url_for, flash, request



@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/studentdetails')
def student_details():
    return render_template('student_details.html')