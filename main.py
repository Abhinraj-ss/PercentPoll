from flask import Flask, request, render_template, redirect, url_for
from flask_login import login_required, current_user
from flask import Blueprint
from . import db

main = Blueprint('main', __name__)
 
@main.route("/" , methods=["GET","POST"])
@login_required
def index():
    return render_template("index.html",name=current_user.username)


@main.route("/create")
def create():
    
    return render_template("create.html")

@main.route("/vote" , methods=["GET","POST"])
def vote():
    title=request.form['title']
    pollOption=request.form.getlist('pollOption[]')
    closing=request.form['closing']
    return render_template("vote.html",
						    title=title,
						    pollOption=pollOption)

@main.route("/view")
def view():
    return render_template("view.html")
	    
