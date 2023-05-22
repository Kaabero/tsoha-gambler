from app import app
from flask import render_template, request, redirect
import fixtures, users

@app.route("/")
def index():
    list = fixtures.get_list()
    return render_template("index.html", fixtures=list)
    

@app.route("/bet")
def bet():
    pass

@app.route("/send", methods=["POST"])
def send():
    pass

@app.route("/scores")
def scores():
    pass

@app.route("/game")
def add_game():
    pass

@app.route("/outcome")
def add_outcome():
    pass

@app.route("/score")
def score():
    pass

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")