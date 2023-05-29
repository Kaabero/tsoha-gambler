from db import db
from sqlalchemy.sql import text
from datetime import datetime

def bet(game_id, user_id, goals_home, goals_visitor):

    sql = text("SELECT date FROM games WHERE id=:game_id")
    date = db.session.execute(sql, {'game_id':game_id})
    
    for row in date:
        if row.date > datetime.now():
        
            try:
                sql = text("INSERT INTO bets (game_id, user_id, goals_home, goals_visitor) VALUES (:game_id, :user_id, :goals_home, :goals_visitor)")
                db.session.execute(sql, {"game_id":game_id, "user_id":user_id, "goals_home":goals_home, "goals_visitor":goals_visitor})
                db.session.commit()
                return True
            except:
                return False
    
    return False