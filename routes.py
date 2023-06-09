from app import app
from flask import render_template, request, redirect
import users, games, bets, scores

@app.route("/")
def index():
    list = games.get_open_games()
    return render_template("index.html", games=list)
    

@app.route("/bet")
def bet():
    list = games.get_open_games()
    return render_template("bet.html", games=list)

@app.route("/score")
def score():
    list = scores.scorable_games()
    return render_template("score.html", games=list)

@app.route("/get_scores")
def get_scores():
    list = scores.get_scores()
    return render_template("get_scores.html", scores=list)

@app.route("/get_total_scores")
def get_total_scores():
    list = scores.get_total_scores()
    return render_template("get_total_scores.html", scores=list)

@app.route("/get_outcomes")
def get_outcomes():
    list = games.get_outcomes()
    return render_template("get_outcomes.html", outcomes=list)

@app.route("/get_bets")
def get_bets():
    list = bets.get_bets()
    return render_template("get_bets.html", bets=list)

@app.route("/own_bets")
def own_bets():
    user_id = users.user_id()
    list = bets.own_bets(user_id)
    return render_template("own_bets.html", bets=list)

@app.route("/front_page", methods=["POST"])
def front_page():
    return redirect("/")

@app.route("/new_game", methods=["POST"])
def new_game():
    home_team = request.form["home_team"]
    visitor_team = request.form["visitor_team"]
    day = request.form["date"]
    time = request.form["time"]
    if games.add_game(home_team, visitor_team, day, time):
        return render_template("successfull_operation.html", message="Peli lisätty onnistuneesti.")
    else:
        return render_template("error.html", message="Pelin lisäys ei onnistunut. Tarkista syötteet.")



@app.route("/new_outcome", methods=["POST"])
def new_outcome():
    game_id = request.form["game_id"]
    goals_home = request.form["goals_home"]
    goals_visitor = request.form["goals_visitor"]
    if games.add_outcome(game_id, goals_home, goals_visitor):
        games.mark_as_registered(game_id)
        return render_template("successfull_operation.html", message="Lopputulos lisätty onnistuneesti.")
    else: 
        return render_template("error.html", message="Lopputuloksen lisäys ei onnistunut. Tarkista syötteet.")

@app.route("/new_bet", methods=["POST"])
def new_bet():
    game_id = request.form["game_id"]
    goals_home = request.form["goals_home"]
    goals_visitor = request.form["goals_visitor"]
    user_id = users.user_id()
    if bets.already_placed_bet(user_id, game_id):
        return render_template("error.html", message="Veikkauksen lisäys ei onnistunut. Sinulla on jo veikkaus tähän peliin.")
    if bets.bet(game_id, user_id, goals_home, goals_visitor):
        return render_template("successfull_operation.html", message="Veikkaus lisätty onnistuneesti.")
    else: 
        return render_template("error.html", message="Veikkauksen lisäys ei onnistunut. Tarkista syötteet.")

@app.route("/delete_bet", methods=["POST"])
def delete_bet():
    user_id = users.user_id()
    game_id = request.form["game_id"]
    if bets.delete_bet(user_id, game_id):
        return render_template("successfull_operation.html", message="Veikkaus poistettu onnistuneesti.")
    else: 
        return render_template("error.html", message="Veikkauksen poisto ei onnistunut. Tarkista veikkaustunnus.")



@app.route("/add_scores", methods=["POST"])
def add_scores():
    allow = False
    if users.is_admin():
        allow = True
        game_id = request.form["game_id"]
        if scores.is_scorable(game_id):
            outcome = games.get_outcome(game_id)
            goals_home = outcome[0]
            goals_visitor = outcome[1]

            correct_bets = scores.correct_bets(game_id, goals_home, goals_visitor)
            for user in correct_bets:
                scores.add_three_points(game_id, user)

            if goals_home > goals_visitor:
                correct_home_wins = scores.home_wins(game_id)

                for user in correct_home_wins:
                    if user not in correct_bets:
                        scores.add_one_point(game_id, user)

            elif goals_home < goals_visitor:
                correct_visitor_wins = scores.visitor_wins(game_id)

                for user in correct_visitor_wins:
                    if user not in correct_bets:
                        scores.add_one_point(game_id, user)
            else:
                correct_draw = scores.draw(game_id)
                for user in correct_draw:
                    if user not in correct_bets:
                        scores.add_one_point(game_id, user)
        
            scores.mark_as_scored(game_id)
            return render_template("successfull_operation.html", message="Pisteytys onnistui.")
        else: 
            return render_template("error.html", message="Pisteytys ei onnistunut. Tarkista syötteet.")
    if not allow:
        return render_template("error.html", message="Ei oikeutta nähdä sivua")

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
        return render_template("error.html", message="Ei oikeutta nähdä sivua")


@app.route("/add_outcome", methods=["GET", "POST"])
def add_outcome():
    allow = False
    if users.is_admin():
        allow = True
        if request.method == "GET":
            list = games.get_closed_games()
            return render_template("add_outcome.html", fixtures=list)
        if request.method == "POST":
            return redirect("/")
    if not allow:
        return render_template("error.html", message="Ei oikeutta nähdä sivua")

@app.route("/new_competition", methods=["GET", "POST"])
def new_competitiom():
    allow = False
    if users.is_admin():
        allow = True
        if request.method == "GET":
            return render_template("new_competition.html")
        if request.method == "POST":
            games.delete_all()
            return render_template("successfull_operation.html", message="Uusi kisa aloitettu.")
    if not allow:
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
        if users.too_short_password(password1):
            return render_template("error.html", message="Salasanan minimipituus on 8 merkkiä.")
        if users.too_short_username(username):
            return render_template("error.html", message="Käyttäjätunnuksen minimipituus on 2 merkkiä.")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut. Käyttäjätunnus on jo käytössä.")
