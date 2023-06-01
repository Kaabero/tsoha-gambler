from db import db
from sqlalchemy.sql import text
from datetime import datetime

def scorable_games():
    sql = text("SELECT * FROM outcomes WHERE scored=0")
    games = db.session.execute(sql).fetchall()
    return games

def is_scorable(game_id):
    try:
        sql = text("SELECT game_id FROM outcomes WHERE scored=0 AND game_id=:game_id")
        game = db.session.execute(sql, {"game_id":game_id}).fetchone()
        if game is not None:
            return True
        else:
            return False
    except:
        return False

def mark_as_scored(game_id):
    sql = text("UPDATE outcomes SET scored=1 WHERE game_id=:game_id")
    db.session.execute(sql, {"game_id":game_id})
    db.session.commit()

def correct_bets(game_id, goals_home, goals_visitor):
    sql = text("SELECT user_id FROM bets WHERE game_id=:game_id AND goals_home=:goals_home AND goals_visitor=:goals_visitor")
    users = db.session.execute(sql, {"game_id":game_id, "goals_home":goals_home, "goals_visitor":goals_visitor }).fetchall()
    
    correct_bets = []

    for user in users:
        correct_bets.append(user[0])
    print(correct_bets)
    return correct_bets


def home_wins(game_id):
    sql = text("SELECT user_id FROM bets WHERE goals_home > goals_visitor AND game_id=:game_id")
    users = db.session.execute(sql, {"game_id":game_id}).fetchall()
    
    correct_home_wins = []

    for user in users:
        correct_home_wins.append(user[0])
   
    return correct_home_wins

def visitor_wins(game_id):
    sql = text("SELECT user_id FROM bets WHERE goals_home < goals_visitor AND game_id=:game_id")
    users = db.session.execute(sql, {"game_id":game_id}).fetchall()
    
    correct_visitor_wins = []

    for user in users:
        correct_visitor_wins.append(user[0])

    print(f"heippa{correct_visitor_wins}")
    return correct_visitor_wins

def add_three_points(game_id, user_id):
    sql = text ("INSERT INTO scores (game_id, user_id, scores) VALUES (:game_id, :user_id, :scores)")
    db.session.execute(sql, {"game_id":game_id, "user_id":user_id, "scores":3})
    db.session.commit()
    return

def add_one_point(game_id, user_id):
    sql = text ("INSERT INTO scores (game_id, user_id, scores) VALUES (:game_id, :user_id, :scores)")
    db.session.execute(sql, {"game_id":game_id, "user_id":user_id, "scores":1})
    db.session.commit()
    return


