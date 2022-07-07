from fcntl import F_GET_SEALS
from multiprocessing import connection
from os import abort
from textwrap import indent
from flask import Flask, jsonify, render_template, request, redirect, session
from sqlalchemy import true
from models import SignupModel, db, StudentModel
# from flask_admin import Admin
from django.http.response import JsonResponse
from flask_admin.contrib.sqla import ModelView
import sqlite3
import jsons
from collections import ChainMap
from typing import Any
import bcrypt

app = Flask(__name__)
# admin = Admin(app)





app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "mysceretkey"
db.init_app(app)

connection = sqlite3.connect("students.db",check_same_thread=False)
cur = connection.cursor()

print(SignupModel.query.all())
