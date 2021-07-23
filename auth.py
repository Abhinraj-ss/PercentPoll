from flask import Flask, request, render_template, redirect, url_for, flash, Blueprint
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
auth = Blueprint('auth', __name__)

@auth.route("/login")
def login():
    next=request.args.get('next', '')
    print(request.args.get('next', ''))
    return render_template('login.html',next=next)
   
    
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route("/register")
def register():
    
    return render_template("register.html")
    
@auth.route('/register', methods=['POST'])
def register_post():
    
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first() 

    if user: 
        flash('Username already exists')
        return redirect(url_for('auth.register'))

    new_user = User(username=username, password=generate_password_hash(password, method='sha256'))

   
    try:
        db.session.add(new_user)
        db.session.commit()
    except:
        return 'Unable to add the user to database.'

    return redirect(url_for('auth.login'))
    

@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(username=username).first()

    
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) 
    next=request.form.get('next')
    print(next)
    if next != "/" and next !=''  :
        x=next
        print(type(x))
        args=x.split('/',4)
        print(args)
        print(type(args))
        login_user(user, remember=remember)
        return redirect(url_for('main.vote',userId=int(args[2]),pollId=int(args[3])))
   
    login_user(user, remember=remember)
    return redirect(url_for('main.index'))
