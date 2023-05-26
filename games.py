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
    