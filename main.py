from flask import Flask, request, render_template, redirect, url_for
from flask_login import login_required, current_user
from flask import Blueprint
from . import db
from .models import Poll

main = Blueprint('main', __name__)
 
@main.route("/" , methods=["GET","POST"])
@login_required
def index():
    return render_template("index.html",name=current_user.username.title())


@main.route("/create")
def create():
    
    return render_template("create.html")
    
@main.route("/create", methods=['POST'])
def create_post():
    title=request.form['title']
    pollOption=request.form.getlist('pollOption[]')
    closing=request.form['closing']
    
    new_poll = Poll(pollId=current_user.id, title=title, option1=pollOption[0],date=closing)
    
  
    try:
        db.session.add(new_poll)
        db.session.commit()
    except:
        return 'Unable to add the user to database.'
        
    return redirect(url_for('main.vote'))

@main.route("/vote" )
def vote():
    poll = Poll.query.filter_by(pollId=current_user.id).first()
    pollOption=[]
    pollOption.append(poll.option1)
    return render_template("vote.html",title=poll.title,pollOption=pollOption)
    
    
@main.route("/vote" , methods=['POST'])
def vote_post():
    
    return redirect(url_for('main.index'))

@main.route("/view")
def view():
    return render_template("view.html")
	    
