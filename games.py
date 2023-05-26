from db import db
from sqlalchemy.sql import text

def add_game(home_team, visitor_team, date, time):
    sql = text("INSERT INTO games (home_team, visitor_team, date, time) VALUES (:home_team, :visitor_team, :date, :time)")
    db.session.execute(sql, {"home_team":home_team, "visitor_team":visitor_team, "date":date, "time":time})
    db.session.commit()
    return True
    