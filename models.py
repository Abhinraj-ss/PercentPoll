from sqlalchemy import Column, Integer, String, ForeignKey, Table
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    username = db.Column(db.String(1000),unique=True)
    password = db.Column(db.String(100))
    polls=db.relationship("Poll",backref='host')
    
    
class Poll( db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pollId=db.Column(db.Integer, db.ForeignKey("user.id"))
    title=db.Column(db.String(30))
    option1 = db.Column(db.String(20))
    date=db.Column(db.String(10))
   
