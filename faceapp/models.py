from flask import Flask
import flask_sqlalchemy
from faceapp import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=10), unique=True, nullable=False)
    email = db.Column(db.String(length=20), unique=True, nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False)



class Student(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    dept = db.Column(db.String(length=10), nullable=False)
    course = db.Column(db.String(length=10), nullable=False)
    year = db.Column(db.String(length=20), nullable=False)
    semester = db.Column(db.Integer(), nullable=False)
    name = db.Column(db.String(length=30), nullable=False)
    section = db.Column(db.String(length=10), nullable=False)
    roll_no = db.Column(db.Integer(), unique=True, nullable=False)
    gender = db.Column(db.String(length=20), nullable=False)
    mobile_no = db.Column(db.String(length=10), nullable=False)
    email = db.Column(db.String(length=20), unique=True, nullable=False)
    teacher = db.Column(db.String(length=20), nullable=False)
    photo_sample = db.Column(db.String(), nullable=False)
