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

    def __init__(self, first_name, last_name, email, contact, password, gender, hobbies, country):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.contact = contact
        self.password = password
        self.gender = gender
        self.hobbies = hobbies
        self.country = country

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

class SignupModel(db.Model):
    __tablename__= "signup"

    username = db.Column(db.String(80),primary_key=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

        def __repr__(self):
            return f"{self.username}"

    