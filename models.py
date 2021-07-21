from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    username = db.Column(db.String(1000),unique=True)
    password = db.Column(db.String(100))

#def init_db():
   # db.create_all()

    # Create a test user
    #new_user = User('abbbb', 'aaaaaaaa')
   # db.session.add(new_user)
    #db.session.commit()


#if __name__ == '__main__':
   # init_db()

