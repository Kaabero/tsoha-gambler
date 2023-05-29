from db import db
from sqlalchemy.sql import text
from datetime import datetime

def scorable_games():
    sql = text("SELECT * FROM outcomes WHERE scored IS NOT 1")
    games = db.session.execute(sql).fetchall()
    db.session.commit()
    return games

def is_scorable(game_id):
    pass
