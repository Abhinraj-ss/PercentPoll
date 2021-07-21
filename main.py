from flask import Flask, request, render_template, redirect, url_for
from flask_login import login_required, current_user
from flask import Blueprint
from . import db
from .models import Poll, Pollings

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
    
    for i in range(len(pollOption),10):
        pollOption.append('NONE')
            
    new_poll = Poll(hostId=current_user.id, title=title,option1=pollOption[0],option2=pollOption[1],option3=pollOption[2],option4=pollOption[3],option5=pollOption[4],option6=pollOption[5],option7=pollOption[6],option8=pollOption[7],option9=pollOption[8],option10=pollOption[9],date=closing)
    
    new_pollings=Pollings(pollId=new_poll.hostId,option1=0,option2=0,option3=0,option4=0,option5=0,option6=0,option7=0,option8=0,option9=0,option10=0)
    db.session.add(new_poll)
    db.session.add(new_pollings)
    print(new_pollings)
    db.session.commit()
        
    
    return redirect(url_for('main.vote'))

@main.route("/vote" )
def vote():
    poll = Poll.query.filter_by(hostId=current_user.id).first()
    pollOption=[]
    pollOption.append(poll.option1)
    pollOption.append(poll.option2)
    pollOption.append(poll.option3)
    pollOption.append(poll.option4)
    pollOption.append(poll.option5)
    pollOption.append(poll.option6)
    pollOption.append(poll.option7)
    pollOption.append(poll.option8)
    pollOption.append(poll.option9)
    pollOption.append(poll.option10)
    return render_template("vote.html",title=poll.title,pollOption=pollOption)
    

   
@main.route("/vote" , methods=['POST'])
def vote_post():
    select = request.form['selected']
    print(select)
    return redirect(url_for('main.index'))
    
    
    
@main.route("/view")
def view():

    return render_template("view.html")
	    


