from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Users(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(255), nullable=False, unique=True)
    Email = db.Column(db.String(255), nullable=False, default="aa@gmail.com")
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
    Status = db.Column(db.String(255), nullable=True)
    Dataset1 = db.Column(db.Text, nullable=False)
    Dataset2 = db.Column(db.Text, nullable=True, default="")
    Dataset3 = db.Column(db.Text, nullable=True, default="")

class Invitations(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.DateTime, nullable=False)
    TeamId = db.Column(db.Integer, db.ForeignKey('users.Id'), nullable=False)
    PersonId = db.Column(db.Integer, db.ForeignKey('users.Id'), nullable=False)
    Status = db.Column(db.String(255), nullable=False)

    team = db.relationship('Users', foreign_keys=[TeamId], backref='sent_invitations')
    person = db.relationship('Users', foreign_keys=[PersonId], backref='received_invitations')

class Selections(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.DateTime, nullable=False)
    TeamId = db.Column(db.Integer, db.ForeignKey('users.Id'), nullable=False)
    TaskId = db.Column(db.Integer, db.ForeignKey('tasks.Id'), nullable=False)
    Status = db.Column(db.String(255), nullable=False)

    team = db.relationship('Users', foreign_keys=[TeamId], backref='sent_selections')
    task = db.relationship('Tasks', foreign_keys=[TaskId], backref='received_selections')