from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Users(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(255), nullable=False, unique=True)
    Password = db.Column(db.Text, nullable=False)
    Role = db.Column(db.String(255), nullable=False, default="User")

    def SetPassword(self, password):
        self.Password = generate_password_hash(password)

    def CheckPassword(self, password):
        return check_password_hash(self.Password, password)
    

# class Courses(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     Title = db.Column(db.String(255), nullable=False, unique=True)
#     HPrice = db.Column(db.Integer, nullable=False)
#     Type = db.Column(db.String(255), nullable=False)