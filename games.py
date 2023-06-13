from datetime import datetime
from sqlalchemy.sql import text
from db import db


def add_game(home_team, visitor_team, day, time):

    if home_team.lower() == visitor_team.lower():
        return False

    splitted_date = day.split("-")
    splitted_time = time.split(":")

    date = datetime(int(splitted_date[0]), int(splitted_date[1]), int(
        splitted_date[2]), int(splitted_time[0]), int(splitted_time[1]))

    if date < datetime.now():
        return False

    sql = text(
        """INSERT INTO games (home_team, visitor_team, date) 
           VALUES (:home_team, :visitor_team, :date)""")
    db.session.execute(sql,
                        {"home_team": home_team,
                        "visitor_team": visitor_team,
                        "date": date})
    db.session.commit()
    return True


def add_outcome(game_id, goals_home, goals_visitor):

    sql = text("SELECT date FROM games WHERE id=:game_id")
    date = db.session.execute(sql, {"game_id": game_id})

    for row in date:
        if row.date < datetime.now():
            try:
                sql = text(
                    """INSERT INTO outcomes (game_id, goals_home, goals_visitor, scored) 
                       VALUES (:game_id, :goals_home, :goals_visitor, :scored)""")
                db.session.execute(sql,
                                   {"game_id": game_id,
                                    "goals_home": goals_home,
                                    "goals_visitor": goals_visitor,
                                    "scored": 0})
                db.session.commit()
                return True
            except BaseException:
                return False
    return False


def get_open_games():
    sql = text(
        """SELECT id, home_team, visitor_team, date, outcome_added 
           FROM games WHERE date BETWEEN NOW() AND date ORDER BY date""")
    games = db.session.execute(sql).fetchall()
    return games


def get_closed_games():
    sql = text(
        """SELECT id, home_team, visitor_team, date, outcome_added 
           FROM games WHERE date < NOW() AND outcome_added is null ORDER BY date""")
    games = db.session.execute(sql).fetchall()
    return games


def get_outcome(game_id):
    sql = text(
        "SELECT goals_home, goals_visitor FROM outcomes WHERE game_id=:game_id")
    goals = db.session.execute(sql, {"game_id": game_id}).fetchall()
    return goals[0]


def mark_as_registered(game_id):
    sql = text("UPDATE games SET outcome_added=1 WHERE id=:game_id")
    db.session.execute(sql, {"game_id": game_id})
    db.session.commit()

def delete_all():
    sql = text("DELETE FROM scores")
    db.session.execute(sql)
    sql = text("DELETE FROM outcomes")
    db.session.execute(sql)
    sql = text("DELETE FROM bets")
    db.session.execute(sql)
    sql = text("DELETE FROM games")
    db.session.execute(sql)
    db.session.commit()

def get_outcomes():
    sql = text("""SELECT G.home_team, G.visitor_team, G.date, O.goals_home, O.goals_visitor
                  FROM outcomes O, games G WHERE O.game_id=G.id ORDER BY G.date""")
    outcomes = db.session.execute(sql).fetchall()
    return outcomes
