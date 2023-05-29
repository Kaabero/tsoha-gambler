from db import db
from sqlalchemy.sql import text
from datetime import datetime

def add_game(home_team, visitor_team, day, time):
    
    splitted_date=day.split("-")
    splitted_time=time.split(":")
    
    date = datetime(int(splitted_date[0]), int(splitted_date[1]), int(splitted_date[2]), int(splitted_time[0]), int(splitted_time[1]))
    
    sql = text("INSERT INTO games (home_team, visitor_team, date) VALUES (:home_team, :visitor_team, :date)")
    db.session.execute(sql, {"home_team":home_team, "visitor_team":visitor_team, "date":date})
    db.session.commit()
    return True

def add_outcome(game_id, goals_home, goals_visitor):

    sql = text("SELECT date FROM games WHERE id=:game_id")
    date = db.session.execute(sql, {'game_id':game_id})

    for row in date:
        if row.date < datetime.now():
            try:    
                sql = text("INSERT INTO outcomes (game_id, goals_home, goals_visitor) VALUES (:game_id, :goals_home, :goals_visitor)")
                db.session.execute(sql, {"game_id":game_id, "goals_home":goals_home, "goals_visitor":goals_visitor})
                db.session.commit()
                return True
            except:
                return False
    return False

def scorable_games():

    sql = text("SELECT * FROM outcomes WHERE scored is null")
    games = db.session.execute(sql).fetchall()
    db.session.commit()
    return games

def get_open_games():
    sql = text("SELECT * FROM games WHERE date BETWEEN NOW() AND date ORDER BY date")
    games = db.session.execute(sql).fetchall()
    db.session.commit()
    return games

def get_closed_games():
    sql = text("SELECT * FROM games WHERE date < NOW() ORDER BY date")
    games = db.session.execute(sql).fetchall()
    db.session.commit()
    return games

