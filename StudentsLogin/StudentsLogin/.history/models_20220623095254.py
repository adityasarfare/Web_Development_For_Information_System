from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class StudentModel(db.Model):
    __tablename__= "students"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    email = db.Column(db.String)
    contact = db.Column(db.Integer)
    password = db.Column(db.String)
    gender = db.Column(db.String)
    hobbies = db.Column(db.String)
    country = db.Column(db.String(80))

    @property
    def serialize(self):
        return {
                'first_name' : self.first_name,
                'last_name' : self.last_name,
                'email' : self.email,
                'contact' : self.contact,
                'password' : self.password,
                'gender' : self.gender,
                'hobbies' : self.hobbies,
                'country' : self.country,
        }

    def __init__(self, first_name, last_name, email, contact, password, gender, hobbies, country):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.contact = contact
        self.password = password
        self.gender = gender
        self.hobbies = hobbies
        self.country = country


class SignupModel(db.Model):
    __tablename__= "signup"

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))

    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

        def __repr__(self):
            return f"{self.username}"

    