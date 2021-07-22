from flask import Flask, request, render_template, redirect, url_for
from flask_login import login_required, current_user
from flask import Blueprint
from datetime import date
from . import db
from .models import Poll, Pollings, Percentpoll

main = Blueprint('main', __name__)
 
@main.route("/" )
@login_required
def index():
    polls = Poll.query.filter_by( hostId=current_user.id).all()
    percents=[]
    for poll in polls:
        percents.append(Percentpoll.query.filter_by( pollId=poll.id).first())
   
    zipped=zip(polls,percents)
    return render_template("index.html",name=current_user.username.title(),zipped_data=zipped)




@main.route("/create")
def create():
    today = date.today()
    date_today = today.strftime("%d/%m/%Y")
    print(date_today)
    
    polls=Poll.query.filter_by(hostId=current_user.id).all()
    
    for poll in polls:
        print(poll.id)
    
    lastPoll = Poll.query.order_by(Poll.id.desc()).first()
    return render_template("create.html",hostId=current_user.id,pollId=lastPoll.id+1)
    
@main.route("/create", methods=['POST'])
def create_post():
    title=request.form['title']
    pollOption=request.form.getlist('pollOption[]')
    closing=request.form['closing']
    
    for i in range(len(pollOption),10):
        pollOption.append('NONE')
            
    new_poll = Poll(hostId=current_user.id, title=title,option1=pollOption[0],option2=pollOption[1],option3=pollOption[2],option4=pollOption[3],option5=pollOption[4],option6=pollOption[5],option7=pollOption[6],option8=pollOption[7],option9=pollOption[8],option10=pollOption[9],date=closing)
    
    new_pollings=Pollings(pollId=new_poll.hostId,option1=0,option2=0,option3=0,option4=0,option5=0,option6=0,option7=0,option8=0,option9=0,option10=0)
    
    new_percentpoll=Percentpoll(pollId=new_poll.hostId,option1=0,option2=0,option3=0,option4=0,option5=0,option6=0,option7=0,option8=0,option9=0,option10=0)
    db.session.add(new_percentpoll)
    db.session.add(new_poll)
    db.session.add(new_pollings)
    db.session.commit()
    return redirect(url_for('main.vote',userId=current_user.id,pollId=new_poll.id))




@main.route("/vote/<userId>/<pollId>" , methods=["GET","POST"])
def vote(userId,pollId):
    poll = Poll.query.filter_by(hostId=userId).first()
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
    if request.method == 'GET':
        return render_template("vote.html",pollId=int(poll.id),title=poll.title,pollOption=pollOption)
    if request.method == 'POST':
        select = request.form['selected']
        index=pollOption.index(select)
        option=f"option{index+1}"
        polling = Pollings.query.filter_by( pollId = poll.id).first()
        percentpoll = Percentpoll.query.filter_by( pollId = poll.id).first()
        sum=polling.option1+polling.option2+polling.option3+polling.option4+polling.option5+polling.option6+polling.option7+polling.option8+polling.option9+polling.option10+1
        
        if option=="option1":
            polling.option1+=1
            
        elif option=="option2":
            polling.option2+=1
            
        elif option=="option3":
            polling.option3+=1
            
        elif option=="option4":
            polling.option4+=1
            
        elif option=="option5":
            polling.option5+=1
            
        elif option=="option6":
            polling.option6+=1
            
        elif option=="option7":
            polling.option7+=1
            
        elif option=="option8":
            polling.option8+=1
            
        elif option=="option9":
            polling.option9+=1
            
        elif option=="option10":
            polling.option10+=1
            
        
        percentpoll.option1=(polling.option1/sum)*100
        percentpoll.option2=(polling.option2/sum)*100   
        percentpoll.option3=(polling.option3/sum)*100    
        percentpoll.option4=(polling.option4/sum)*100
        percentpoll.option5=(polling.option5/sum)*100
        percentpoll.option6=(polling.option6/sum)*100
        percentpoll.option7=(polling.option7/sum)*100
        percentpoll.option8=(polling.option8/sum)*100
        percentpoll.option9=(polling.option9/sum)*100
        percentpoll.option10=(polling.option10/sum)*100
           
        print(polling.option1)
        print(percentpoll.option1)
        print(polling.option2)
        print(percentpoll.option2)
        print(polling.option3)
        print(percentpoll.option3)
        print(polling.option4)
        print(percentpoll.option4)
        print(polling.option5)
        print(percentpoll.option5)
        print(polling.option6)
        print(percentpoll.option6)
        print(polling.option7)
        print(percentpoll.option7)
        print(polling.option8)
        print(percentpoll.option8)
        print(polling.option9)
        print(percentpoll.option9)
        print(polling.option10)
        print(percentpoll.option10)
            
            
        db.session.commit()   
        return redirect(url_for('main.index'))
   

    
    
    
@main.route("/view")
def view():
    poll = Poll.query.filter_by( hostId=current_user.id).first()
    percent=Percentpoll.query.filter_by( pollId=poll.id).first()
    return render_template("view.html",poll=poll,percent=percent)
	    


