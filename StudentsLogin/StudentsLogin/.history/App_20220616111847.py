
from fcntl import F_GET_SEALS
from os import abort
from tokenize import Ignore
from flask import Flask, jsonify, render_template, request, redirect, session
from sqlalchemy import true
from models import SignupModel, db, StudentModel
# from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import jsons
import warnings

app = Flask(__name__)
# admin = Admin(app)



warnings.filterwarnings(action='ignore')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "mysceretkey"
db.init_app(app)

is_Admin = False

class SecureModelView(ModelView):
    def is_accessible(Self):
        if "logged_in" in session:
            return True
        else:
            abort(403)

# admin.add_view(SecureModelView(Posts, db.session))

@app.before_first_request
def create_table():
    db.create_all()

@app.route('/app/create', methods = ['GET', 'POST'])
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
        return redirect('/app/students')

@app.route('/app/signup', methods = ['GET','POST'])
def signup():
    if request.method=='GET':
        return render_template("signup.html")
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        users = SignupModel(
            username = username,
            email = email,
            password = password
        )
        db.session.add(users)
        db.session.commit()
        return redirect('/app/login')

@app.route('/app/students', methods = ['GET', 'POST'])
def RetrieveList():
    students = StudentModel.query.all()
    print(jsons.dump(students[0]))
    return render_template('index.html', students = students, can_edit = is_Admin)





@app.route('/app/<int:id>/edit', methods=['GET', 'POST'])
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
        return redirect('/app/students')
        return f"Student with id = {id} Does nit exist"
            
    return render_template('update.html', students = students)

@app.route('/app/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    students = StudentModel.query.filter_by(id=id).first()
    if request.method == 'POST':
        if students:
           db.session.delete(students)
           db.session.commit()
           print(jsonify(StudentModel.query.all))
           return redirect('/students')
        abort(404)
    return render_template('delete.html')

@app.route('/app/', methods=['GET', 'POST'])
@app.route("/app/login/", methods=['GET', 'POST'])
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

@app.route("/app/admin/", methods= ['GET','POST'])
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



@app.route("/app/logout")
def logout():
    session.clear()
    return redirect("/students")




app.run(host= 'localhost', port=5000)

# @app.route("/hello")
# def hello_world():
#     return "<p>Hello, World!</p>"

# app.run(host= 'localhost', port=5000)