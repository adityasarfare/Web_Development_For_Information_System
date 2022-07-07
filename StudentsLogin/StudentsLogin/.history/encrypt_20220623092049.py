from fcntl import F_GET_SEALS
from multiprocessing import connection
from os import abort
from textwrap import indent
from django.template import engines
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
from sqlalchemy import create_engine
app = Flask(__name__)
# admin = Admin(app)





app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "mysceretkey"
db.init_app(app)

connection = sqlite3.connect("students.db",check_same_thread=False)
engines = create_engine("sqlite:///students.db",echo=False)
cur = connection.cursor()

import pandas as pd

table = pd.read_sql_table(table_name="signup",con=engines)
table  = pd.concat('bharath','b@gmail.com','123456')
table = pd.DataFrame(table)
print(table)
val = table[table['username'] == 'bharath']
a = val['password']
print(a)