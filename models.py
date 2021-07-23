from sqlalchemy import Column, Integer, String, ForeignKey, Table
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,unique=True) 
    username = db.Column(db.String(1000),unique=True)
    password = db.Column(db.String(100))
    polls=db.relationship("Poll",backref='host')
    
    
class Poll( db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,unique=True)
    hostId=db.Column(db.Integer, db.ForeignKey("user.id"))
    title=db.Column(db.String(30))
    option1 = db.Column(db.String(20))
    option2 = db.Column(db.String(20))
    option3 = db.Column(db.String(20))
    option4 = db.Column(db.String(20))
    option5 = db.Column(db.String(20))
    option6 = db.Column(db.String(20))
    option7 = db.Column(db.String(20))
    option8 = db.Column(db.String(20))
    option9 = db.Column(db.String(20))
    option10 = db.Column(db.String(20))
    date=db.Column(db.String(20))
    pollings=db.relationship("Pollings",backref='poll')
    pollings=db.relationship("Percentpoll",backref='poll')
 
class Pollings(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,unique=True)
    pollId=db.Column(db.Integer, db.ForeignKey("poll.id"))
    option1 = db.Column(db.Integer)
    option2 = db.Column(db.Integer)
    option3 = db.Column(db.Integer)
    option4 = db.Column(db.Integer)
    option5 = db.Column(db.Integer)
    option6 = db.Column(db.Integer)
    option7 = db.Column(db.Integer)
    option8 = db.Column(db.Integer)
    option9 = db.Column(db.Integer)
    option10 = db.Column(db.Integer)
    
    
    
class Percentpoll(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,unique=True)
    pollId=db.Column(db.Integer, db.ForeignKey("poll.id"))
    option1 = db.Column(db.Integer)
    option2 = db.Column(db.Integer)
    option3 = db.Column(db.Integer)
    option4 = db.Column(db.Integer)
    option5 = db.Column(db.Integer)
    option6 = db.Column(db.Integer)
    option7 = db.Column(db.Integer)
    option8 = db.Column(db.Integer)
    option9 = db.Column(db.Integer)
    option10 = db.Column(db.Integer)
