from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Users(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(255), nullable=False, unique=True)
    Password = db.Column(db.String(255), nullable=False)
    Role = db.Column(db.String(255), nullable=False, default="User")

    def SetPassword(self, password):
        self.Password = generate_password_hash(password)

    def CheckPassword(self, password):
        return check_password_hash(self.Password, password)
    

class Tasks(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Category = db.Column(db.String(255), nullable=False, unique=True)
    Section = db.Column(db.String(255), nullable=False)
    Code = db.Column(db.String(255), nullable=False)
    Disease = db.Column(db.String(255), nullable=False)
    Dataset1 = db.Column(db.Text, nullable=False)
    Dataset2 = db.Column(db.Text, nullable=True, default="")
    Dataset3 = db.Column(db.Text, nullable=True, default="")