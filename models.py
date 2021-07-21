from sqlalchemy import Column, Integer, String, ForeignKey, Table
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,unique=True) # primary keys are required by SQLAlchemy
    username = db.Column(db.String(1000),unique=True)
    password = db.Column(db.String(100))
    polls=db.relationship("Poll",backref='host')
    
    
class Poll( db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,unique=True)
    pollId=db.Column(db.Integer, db.ForeignKey("user.id"))
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
   
