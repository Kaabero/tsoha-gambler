from app import app
from flask import render_template, request, redirect
import fixtures, users, games

@app.route("/")
def index():
    list = fixtures.get_open_games()
    return render_template("index.html", fixtures=list)
    

@app.route("/bet")
def bet():
    pass

@app.route("/delete")
def delete():
    pass

@app.route("/send", methods=["POST"])
def send():
    home_team = request.form["home_team"]
    visitor_team = request.form["visitor_team"]
    day = request.form["date"]
    time = request.form["time"]
    games.add_game(home_team, visitor_team, day, time)
    return redirect("/")


@app.route("/scores")
def scores():
    pass

@app.route("/add_game", methods=["GET", "POST"])
def add_game():
    allow = False
    if users.is_admin():
        allow = True
        if request.method == "GET":
            return render_template("add_game.html")
        if request.method == "POST":
            return redirect("/")
    if not allow:
        return render_template("error.html", error="Ei oikeutta nähdä sivua")

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
