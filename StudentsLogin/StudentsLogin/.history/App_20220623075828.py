
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

from cryptography.fernet import Fernet
app = Flask(__name__)
# admin = Admin(app)





app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "mysceretkey"
db.init_app(app)

connection = sqlite3.connect("students.db",check_same_thread=False)
cur = connection.cursor()


is_Admin = False

class SecureModelView(ModelView):
    def is_accessible(Self):
        if "logged_in" in session:
            return True
        else:
            abort(403)

from flask import json
class ModelEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if hasattr(o, 'to_json'):
            return o.to_json()
        else:
            return super(ModelEncoder, self).default(o)

app.json_encoder = ModelEncoder

# admin.add_view(SecureModelView(Posts, db.session))

@app.before_first_request
def create_table():
    db.create_all()

@app.route('/create', methods = ['GET', 'POST'])
def create():

    if request.method == 'GET':
        return render_template('create.html')  

    if request.method == 'POST':
        hobby = request.form.getlist('hobbies')
        hobbies =",".join(map(str, hobby))  
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        contact = request.form['contact']
        password = request.form['password']
        gender = request.form['gender']
        hobbies = hobbies
        country = request.form['country']
        
        print(first_name)
        
        students = StudentModel(
            first_name =  first_name,
            last_name = last_name,
            email = email,
            contact = contact,
            password = password,
            gender = gender,
            hobbies = hobbies,
            country  = country 
        )

        db.session.add(students)
        db.session.commit()
        return redirect('/students')

@app.route('/api/create', methods = ['GET', 'POST'])
def api_create():  
    
    if request.method == 'POST':

        data = request.get_data()
        data = json.loads(data.decode('utf-8'))
        print(data, type(data))
        

        id = data.get('id')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        contact = data.get('contact')
        password = data.get('password')
        gender = data.get('gender')
        hobbies = data.get('hobbies')
        country = data.get('country')

        cur.execute("INSERT INTO students (first_name,last_name,email,contact,password,gender,hobbies,country) values (?,?,?,?,?,?,?,?)",
        (first_name,last_name,email,contact,password,gender,hobbies,country))
        connection.commit()

        result = cur.execute("SELECT * FROM students")
        result = result.fetchall()
        col_name=["id","first_name","last_name","email","contact","password","gender","hobbies","country"]
        result_dict = []

        for i in result:
            diction = dict(zip(col_name,i))
            result_dict.append(diction)

        return json.dumps(result_dict,indent=2)

@app.route('/signup', methods = ['GET','POST'])
def signup():
    if request.method=='GET':
        return render_template("signup.html")
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        key = Fernet.generate_key()
        fernet = Fernet(key)

        password = fernet.encrypt(password.encode())

        users = SignupModel(
            username = username,
            email = email,
            password = password
        )
        db.session.add(users)
        db.session.commit()
        return redirect('/login')

@app.route('/students', methods = ['GET', 'POST'])
def RetrieveList():
    students = StudentModel.query.all()
    return render_template('index.html', students = students, can_edit = is_Admin)

@app.route('/api/students', methods = ['GET', 'POST'])
def api_RetrieveList():
    if request.method=='GET':
        result = cur.execute("SELECT * FROM students")
        result = result.fetchall()
        col_name=["id","first_name","last_name","email","contact","password","gender","hobbies","country"]
        result_dict = []
        for i in result:
            diction = dict(zip(col_name,i))
            result_dict.append(diction)
        
        return json.dumps(result_dict,indent=2)



@app.route('/<int:id>/edit', methods=['GET', 'POST'])
def update(id):
    students = StudentModel.query.filter_by(id=id).first()

    if request.method == 'POST':
        if students:
           db.session.delete(students)
           db.session.commit()
       
        hobby = request.form.getlist('hobbies')
        #hobbies = ','.join(map(str, hobby))
        hobbies =  ",".join(map(str, hobby)) 
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        contact = request.form['contact']
        password = request.form['password']
        gender = request.form['gender']
        hobbies = hobbies 
        country = request.form['country']

        students = StudentModel(
            first_name=first_name,
            last_name=last_name,
            email=email,
            contact = contact,
            password=password,
            gender=gender, 
            hobbies=hobbies,
            country = country
        )

        db.session.add(students)
        db.session.commit()
        return redirect('/students')
        return f"Student with id = {id} Does nit exist"
            
    return render_template('update.html', students = students)

@app.route('/api/<int:id>/edit', methods=['GET', 'POST'])
def api_update(id):

    students = StudentModel.query.filter_by(id=id).first()
    if request.method == 'POST':

        data = request.get_data()
        data = json.loads(data.decode('utf-8'))
        print(data, type(data))
        

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        contact = data.get('contact')
        password = data.get('password')
        gender = data.get('gender')
        hobbies = data.get('hobbies')
        country = data.get('country')

        if not first_name:
            first_name = students.first_name
        if not last_name:
            last_name = students.last_name
        if not email:
            email = students.email
        if not contact:
            contact = students.contact
        if not password:
            password = students.password
        if not gender:
            gender = students.gender
        if not hobbies:
            hobbies = students.hobbies
        if not country:
            country = students.country

        cur.execute("UPDATE students SET first_name = ?, last_name = ?, email = ?, contact = ?, password = ?, gender = ?, hobbies = ?, country = ? WHERE id = ?",
                    (first_name,last_name,email,contact,password,gender,hobbies,country,id))

        connection.commit()

        result = cur.execute("SELECT * FROM students WHERE id = ?", str(id))
        result = result.fetchall()
        col_name=["id","first_name","last_name","email","contact","password","gender","hobbies","country"]
        result_dict = []

        for i in result:
            diction = dict(zip(col_name,i))
            result_dict.append(diction)

        return json.dumps(result_dict,indent=2)

@app.route('/<int:id>/delete', methods=['GET', 'POST', 'DELETE'])
def delete(id):
    students = StudentModel.query.filter_by(id=id).first()
    if request.method == 'POST':
        if students:
           db.session.delete(students)
           db.session.commit()
           return redirect('/students')
        abort(404)
    return render_template('delete.html')

@app.route('/api/<int:id>/delete', methods=['GET', 'POST', 'DELETE'])
def api_delete(id):
    students = StudentModel.query.filter_by(id=id).first()
    if request.method == 'DELETE':
        if students:
           db.session.delete(students)
           db.session.commit()
        result = cur.execute("SELECT * FROM students")
        result = result.fetchall()
        col_name=["id","first_name","last_name","email","contact","password","gender","hobbies","country"]
        result_dict = []
        for i in result:
            diction = dict(zip(col_name,i))
            result_dict.append(diction)

        return json.dumps(result_dict,indent=2)

@app.route('/api/delete', methods=['GET', 'POST'])
def api_delete_all():
    result = cur.execute("DELETE FROM students")
    data = {"response":"Table has been truncated successfully"}
    return jsonify(data)

@app.route('/', methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        global is_Admin
        login = SignupModel.query.filter_by(username=uname, password=pwd).first()
        if login is not None:
           session['logged_in'] = True
           students = StudentModel.query.all()
           is_Admin = False
           return render_template('adminpage.html', students = students, can_edit=is_Admin)
        else:
           return render_template('login.html', failed = True)
    return render_template('login.html')

@app.route("/admin/", methods= ['GET','POST'])
def admin():
    if request.method == 'POST':
        global is_Admin
        if request.form.get("username") == "admin" and request.form.get("password") == "admin":
           session['logged_in'] = True
           students = StudentModel.query.all()
           is_Admin = True
           return render_template('adminpage.html', students = students, can_edit=is_Admin)
        else:
           return render_template('admin.html', failed = True)
    return render_template('admin.html')



@app.route("/logout")
def logout():
    db.session.close.all()
    session.clear()

    return redirect("/students")




app.run(host= 'localhost', port=5000)

# @app.route("/hello")
# def hello_world():
#     return "<p>Hello, World!</p>"

# app.run(host= 'localhost', port=5000)