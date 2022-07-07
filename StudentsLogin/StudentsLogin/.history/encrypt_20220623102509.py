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
import base64
from collections import ChainMap
from typing import Any
from cryptography.fernet import Fernet
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


uname = "Bharath"
email = "b@gmail.com"
pwd = "1234567"

password = pwd.encode("utf-8")
encoded = base64.b64encode(password)
print(encoded)

table = pd.read_sql_table(table_name="signup",con=engines)
table = pd.DataFrame(table)
print(table)

result = cur.execute("SELECT * FROM signup WHERE username = 'Bharath'")
result = cur.fetchall()
usname=""
passw = ""
for i in result:
        print(base64.b64decode(i[3]))
        