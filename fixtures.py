from db import db
from sqlalchemy.sql import text
from datetime import datetime

def get_open_games():
    sql = text("SELECT * FROM games WHERE date BETWEEN NOW() AND date ORDER BY date")
    fixtures = db.session.execute(sql).fetchall()
    db.session.commit()
    return fixtures

def add_game():
    pass

