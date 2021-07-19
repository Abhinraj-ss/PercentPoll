
from flask import Flask, request, render_template, redirect, url_for

import psycopg2

app = Flask("percentpoll")

@app.route("/" , methods=["GET","POST"])
def index():
    return render_template("index.html")

@app.route("/dashboard" , methods=["GET","POST"])
def dashboard():
    return render_template("dashboard.html")


@app.route("/login")
def login():
    
    return redirect(url_for(".dashboard"))
   
    
@app.route("/logout")
def logout():
    return redirect(url_for(".index"))


@app.route("/register", methods=["GET","POST"])
def register():
    
    return render_template("register.html")

@app.route("/create")
def create():
	
	return render_template("create.html")

@app.route("/vote" , methods=["GET","POST"])
def vote():
	title=request.form['title']
	pollOption=request.form.getlist('pollOption[]')
	closing=request.form['closing']
	print(f"{title} {pollOption} {type(closing)}")
	return render_template("vote.html",
							title=title,
							pollOption=pollOption)

@app.route("/view")
def veiw():
	return render_template("view.html")
	

