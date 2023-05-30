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
