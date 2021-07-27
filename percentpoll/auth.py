from flask import Flask, request, render_template, redirect, url_for, flash, Blueprint
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User,Poll
from . import db
import datetime
auth = Blueprint('auth', __name__)


@auth.route("/login", methods=["GET","POST"])
def login():
    
    
    if request.method == 'GET':
    
        next=request.args.get('next', '')
        return render_template('login.html',next=next)
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = User.query.filter_by(username=username).first()
        today = datetime.datetime.now() 
        polls = Poll.query.filter_by( hostId=user.id, closed=False).all()
        for poll in polls:
            if poll.date<=today:
                poll.closed=True
        next=request.form.get('next')
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login',next=next))
        args=next.split('/',4) 
        
        if next != "/" and next !='' and args[1] == "vote" :
            if int(args[2])!=user.id:
                login_user(user, remember=remember)
                return redirect(url_for('main.vote',hostId=int(args[2]),pollId=int(args[3])))  
            
            else:
                message="Host can't participate in the poll !!!"
                login_user(user, remember=remember)
                current_count = len(Poll.query.filter_by( hostId=user.id, closed=False).all())
                closed_count = len(Poll.query.filter_by( hostId=user.id, closed=True).all())
                return render_template('index.html',message=message,first=True,borderColor="red", user=user.name.title(),current_count=current_count,closed_count=closed_count)
        elif len(args)==2 and args[0]!='':
            login_user(user, remember=remember)
            return redirect(url_for('main.vote',hostId=int(args[0]),pollId=int(args[1])))
    login_user(user, remember=remember)
    current_count = len(Poll.query.filter_by( hostId=user.id, closed=False).all())
    closed_count = len(Poll.query.filter_by( hostId=user.id, closed=True).all())
    return render_template("index.html",first=True, user=user.name.title(),current_count=current_count,closed_count=closed_count)
    
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route("/register", methods=["GET","POST"])
def register():
    if request.method == 'GET':
        next=request.args.get('next', '')
        return render_template('register.html',next=next)
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first() 
        next=request.form.get('next')
        
        if user: 
            flash('Username already exists')
            return redirect(url_for('auth.register',next=next))

        new_user = User(name=name, username=username, password=generate_password_hash(password, method='sha256'))

       
        db.session.add(new_user)
        db.session.commit()
        

        return redirect(url_for('auth.login',next=next))

  
