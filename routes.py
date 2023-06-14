from flask import render_template, request, redirect
from app import app
import users
import games
import bets
import scores


@app.route("/")
def index():
    open_games = games.get_open_games()
    return render_template("index.html", games=open_games)


@app.route("/bet")
def bet():
    open_games = games.get_open_games()
    return render_template("bet.html", games=open_games)


@app.route("/score")
def score():
    scorable_games = scores.scorable_games()
    return render_template("score.html", games=scorable_games)


@app.route("/get_scores")
def get_scores():
    all_scores = scores.get_scores()
    return render_template("get_scores.html", scores=all_scores)


@app.route("/get_total_scores")
def get_total_scores():
    total_scores = scores.get_total_scores()
    return render_template("get_total_scores.html", scores=total_scores)


@app.route("/get_outcomes")
def get_outcomes():
    outcomes = games.get_outcomes()
    return render_template("get_outcomes.html", outcomes=outcomes)


@app.route("/get_bets")
def get_bets():
    all_bets = bets.get_bets()
    return render_template("get_bets.html", bets=all_bets)


@app.route("/get_own_bets")
def get_own_bets():
    user_id = users.user_id()
    own_bets = bets.own_bets(user_id)
    return render_template("get_own_bets.html", bets=own_bets)


@app.route("/front_page", methods=["POST"])
def front_page():
    return redirect("/")


@app.route("/new_bet", methods=["POST"])
def new_bet():
    if not request.form["game_id"]:
        return render_template(
            "error.html",
            message="Veikkauksen lisäys ei onnistunut. Syötä veikkaustunnus.")
    game_id = request.form["game_id"]
    goals_home = request.form["goals_home"]
    goals_visitor = request.form["goals_visitor"]
    user_id = users.user_id()
    if bets.already_placed_bet(user_id, game_id):
        return render_template(
            "error.html",
            message="Veikkauksen lisäys ei onnistunut. Sinulla on jo veikkaus tähän peliin.")
    if bets.bet(game_id, user_id, goals_home, goals_visitor):
        return render_template(
            "successfull_operation.html",
            message="Veikkaus lisätty onnistuneesti.")

    return render_template(
        "error.html",
        message="Veikkauksen lisäys ei onnistunut. Tarkista syötteet.")


@app.route("/delete_bet", methods=["POST"])
def delete_bet():
    user_id = users.user_id()
    if not request.form["game_id"]:
        return render_template(
            "error.html",
            message="Veikkauksen lisäys ei onnistunut. Syötä veikkaustunnus.")
    game_id = request.form["game_id"]
    if bets.delete_bet(user_id, game_id):
        return render_template(
            "successfull_operation.html",
            message="Veikkaus poistettu onnistuneesti.")

    return render_template(
        "error.html",
        message="Veikkauksen poisto ei onnistunut. Tarkista veikkaustunnus.")


@app.route("/add_scores", methods=["POST"])
def add_scores():
    if users.is_admin():
        if not request.form["game_id"]:
            return render_template(
                "error.html",
                message="Veikkauksen lisäys ei onnistunut. Syötä veikkaustunnus.")
        game_id = request.form["game_id"]
        if scores.is_scorable(game_id):
            outcome = games.get_outcome(game_id)
            goals_home = outcome[0]
            goals_visitor = outcome[1]

            correct_bets = scores.correct_bets(
                game_id, goals_home, goals_visitor)
            for user in correct_bets:
                scores.add_three_points(game_id, user)

            if goals_home > goals_visitor:
                correct_home_wins = scores.home_wins(game_id)
                scores.block_double_points(
                    correct_bets, correct_home_wins, game_id)

            elif goals_home < goals_visitor:
                correct_visitor_wins = scores.visitor_wins(game_id)
                scores.block_double_points(
                    correct_bets, correct_visitor_wins, game_id)

            else:
                correct_draw = scores.draw(game_id)
                scores.block_double_points(correct_bets, correct_draw, game_id)

            scores.mark_as_scored(game_id)
            return render_template(
                "successfull_operation.html",
                message="Pisteytys onnistui.")

        return render_template(
            "error.html",
            message="Pisteytys ei onnistunut. Tarkista syötteet.")
    return render_template("error.html", message="Ei oikeutta nähdä sivua")


@app.route("/add_game", methods=["GET", "POST"])
def add_game():
    if users.is_admin():
        if request.method == "GET":
            return render_template("add_game.html")
        if request.method == "POST":
            home_team = request.form["home_team"]
            visitor_team = request.form["visitor_team"]
            day = request.form["date"]
            time = request.form["time"]

            if games.add_game(home_team, visitor_team, day, time):
                return render_template(
                    "successfull_operation.html",
                    message="Peli lisätty onnistuneesti.")

            return render_template(
                "error.html",
                message="Pelin lisäys ei onnistunut. Tarkista syötteet.")

    return render_template("error.html", message="Ei oikeutta nähdä sivua")


@app.route("/add_outcome", methods=["GET", "POST"])
def add_outcome():
    if users.is_admin():
        if request.method == "GET":
            fixtures = games.get_closed_games()
            return render_template("add_outcome.html", fixtures=fixtures)
        if request.method == "POST":
            if not request.form["game_id"]:
                return render_template(
                    "error.html",
                    message="Veikkauksen lisäys ei onnistunut. Syötä veikkaustunnus.")
            game_id = request.form["game_id"]
            goals_home = request.form["goals_home"]
            goals_visitor = request.form["goals_visitor"]
            if games.add_outcome(game_id, goals_home, goals_visitor):
                games.mark_as_registered(game_id)
                return render_template(
                    "successfull_operation.html",
                    message="Lopputulos lisätty onnistuneesti.")
            return render_template(
                "error.html",
                message="Lopputuloksen lisäys ei onnistunut. Tarkista syötteet.")
    return render_template("error.html", message="Ei oikeutta nähdä sivua")


@app.route("/new_competition", methods=["GET", "POST"])
def new_competitiom():
    if users.is_admin():
        if request.method == "GET":
            return render_template("new_competition.html")
        if request.method == "POST":
            games.delete_all()
            return render_template(
                "successfull_operation.html",
                message="Uusi kisa aloitettu.")
    return render_template("error.html", message="Ei oikeutta nähdä sivua")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")

        return render_template(
            "error.html", message="Väärä tunnus tai salasana")
    return render_template(
        "error.html", message="Odottamaton virhe.")


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
        if users.too_short_password(
                password1) or users.too_short_username(username):
            return render_template(
                "error.html",
                message="""Syötä käyttäjätunnus, jonka pituus on vähintään 2 merkkiä
                           ja salasana, jonka pituus on vähintään 8 merkkiä.""")
        if users.register(username, password1):
            return redirect("/")
        return render_template(
            "error.html",
            message="Rekisteröinti ei onnistunut. Käyttäjätunnus on jo käytössä.")
    return render_template(
        "error.html", message="Odottamaton virhe.")
