# main.py
from flask import Flask, request, render_template, redirect, url_for

app = Flask("percentpoll")

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/login")
def login():
    return redirect(url_for(".dashboard"))


@app.route("/logout")
def logout():
    return redirect(url_for(".index"))

@app.route("/create")
def create():
	return render_template("create.html")

@app.route("/vote")
def vote():
	return render_template("vote.html")

if __name__ == "__main__":
    app.run()
