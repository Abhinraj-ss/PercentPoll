from flask import Flask, request, render_template, redirect, url_for
from flask_login import login_required, current_user
from flask import Blueprint
import datetime
from . import db
from .models import Poll, Pollings, Percentpoll

main = Blueprint('main', __name__)
 
@main.route("/" )
@login_required
def index():
    today = datetime.datetime.now() 
    polls = Poll.query.filter_by( hostId=current_user.id, closed=False).all()
    for poll in polls:
        if poll.date<=today:
            poll.closed=True
    
    current_count = len(Poll.query.filter_by( hostId=current_user.id, closed=False).all())
    closed_count = len(Poll.query.filter_by( hostId=current_user.id, closed=True).all())
    return render_template("index.html", user=current_user.name.title(),current_count=current_count,closed_count=closed_count)



@main.route("/create", methods=["GET","POST"])
def create():
    if request.method == 'GET':
    
        current_count = len(Poll.query.filter_by( hostId=current_user.id, closed=False).all())
        closed_count = len(Poll.query.filter_by( hostId=current_user.id, closed=True).all())
        polls=Poll.query.filter_by(hostId=current_user.id).all()
        lastPoll = Poll.query.order_by(Poll.id.desc()).first()
        if polls:
            return render_template("create.html",hostId=current_user.id,pollId=lastPoll.id+1,current_count=current_count,closed_count=closed_count)
        return render_template("create.html",hostId=current_user.id,pollId=1,current_count=current_count,closed_count=closed_count)
    
    if request.method == 'POST':
    
        title=request.form['title']
        pollOption=request.form.getlist('pollOption[]')
        date=request.form['date']
        time=request.form['time']
        closing=date+" "+time
        closing_date=datetime.datetime.strptime(closing, '%Y-%m-%d %H:%M')
        for i in range(len(pollOption),10):
            pollOption.append('NONE')
                
        new_poll = Poll(hostId=current_user.id, title=title,option1=pollOption[0],option2=pollOption[1],option3=pollOption[2],option4=pollOption[3],option5=pollOption[4],option6=pollOption[5],option7=pollOption[6],option8=pollOption[7],option9=pollOption[8],option10=pollOption[9],date=closing_date,closed=False)
  
        new_pollings=Pollings(pollId=new_poll.id,option1=0,option2=0,option3=0,option4=0,option5=0,option6=0,option7=0,option8=0,option9=0,option10=0)
        
        new_percentpoll=Percentpoll(pollId=new_poll.hostId,option1=0,option2=0,option3=0,option4=0,option5=0,option6=0,option7=0,option8=0,option9=0,option10=0)
        db.session.add(new_percentpoll)
        db.session.add(new_poll)
        db.session.add(new_pollings)
        db.session.commit()
        return redirect(url_for('main.index'))




@main.route("/vote/<hostId>/<pollId>" , methods=["GET","POST"])
@login_required
def vote(hostId,pollId):
    poll = Poll.query.filter_by(id=pollId,hostId=hostId).first()
    if poll!=None:
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
        polling = Pollings.query.filter_by( id = poll.id).first()
        voters=polling.voters.split(';')
    
    if request.method == 'GET':
        today = datetime.datetime.now()
        current_count = len(Poll.query.filter_by( hostId=current_user.id, closed=False).all())
        closed_count = len(Poll.query.filter_by( hostId=current_user.id, closed=True).all())
        if poll!=None:
            if poll.date<=today:
                poll.closed=True
                message="Requested Poll has been closed."
                return render_template('index.html',message=message,first=True, user=current_user.username.title(),borderColor="red",current_count=current_count,closed_count=closed_count)
            elif current_user.id in voters:
                message="Your have already responded."
                return render_template('index.html',message=message,first=True, user=current_user.username.title(),borderColor="red",current_count=current_count,closed_count=closed_count)
            
            return render_template("vote.html",hostId=hostId,pollId=poll.id,title=poll.title,pollOption=pollOption,current_count=current_count,closed_count=closed_count)
        return render_template('error.html',first=True,current_count=current_count,closed_count=closed_count)
    
    if request.method == 'POST':
        current_count = len(Poll.query.filter_by( hostId=current_user.id, closed=False).all())
        closed_count = len(Poll.query.filter_by( hostId=current_user.id, closed=True).all())
        select = request.form['selected']
        if select=="Select":
            message="Please select any of the option given !!!"
            return render_template("vote.html",hostId=hostId,pollId=poll.id,title=poll.title,pollOption=pollOption,message=message,current_count=current_count,closed_count=closed_count)
        index=pollOption.index(select)
        option=f"option{index+1}"
        polling = Pollings.query.filter_by( id = poll.id).first()
        percentpoll = Percentpoll.query.filter_by( id = poll.id).first()
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
            
        polling.voters+=(';'+str(current_user.id))
        
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
        
        db.session.commit()   
        message="Your response has been recorded."
        return render_template("index.html", message=message ,first=True, user=current_user.username.title(),borderColor="#28A828",,current_count=current_count,closed_count=closed_count)
   

    
    
    
@main.route("/view")
def view():
    today = datetime.datetime.now() 
    date_today = today.strftime("%d/%m/%Y")
    polls = Poll.query.filter_by( hostId=current_user.id, closed=False).all()
    for poll in polls:
        if poll.date<=today:
            poll.closed=True
    current_count = len(Poll.query.filter_by( hostId=current_user.id, closed=False).all())
    closed_count = len(Poll.query.filter_by( hostId=current_user.id, closed=True).all())
    polls = Poll.query.filter_by( hostId=current_user.id, closed=True).all()
    percents=[]
    
    for poll in polls:
        percents.append(Percentpoll.query.filter_by( id=poll.id).first())
    current=zip(polls,percents)
    return render_template("view.html",page="CLOSED POLLS",polls=len(polls), current_polls=current,current_count=current_count,closed_count=closed_count)
	    
@main.route("/current")
def current():
    today = datetime.datetime.now() 
    date_today = today.strftime("%d/%m/%Y")
    polls = Poll.query.filter_by( hostId=current_user.id, closed=False).all()
    for poll in polls:
        if poll.date<=today:
            poll.closed=True
    current_count = len(Poll.query.filter_by( hostId=current_user.id, closed=False).all())
    closed_count = len(Poll.query.filter_by( hostId=current_user.id, closed=True).all())
    polls = Poll.query.filter_by( hostId=current_user.id, closed=False).all()
    percents=[]
    
    for poll in polls:
        percents.append(Percentpoll.query.filter_by( id=poll.id).first())
    current=zip(polls,percents)
    return render_template("view.html",page="CURRENT POLLLS",polls=len(polls),current_polls=current,current_count=current_count,closed_count=closed_count)
    
    
@main.route("/invalidPoll")
def invalidPoll():
    current_count = len(Poll.query.filter_by( hostId=current_user.id, closed=False).all())
    closed_count = len(Poll.query.filter_by( hostId=current_user.id, closed=True).all())
    render_template("error.html",current_count=current_count,closed_count=closed_count)

