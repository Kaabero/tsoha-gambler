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

def already_placed_bet(user_id, game_id):

    sql = text("SELECT user_id, game_id FROM bets WHERE game_id=:game_id AND user_id=:user_id")
    already_placed_bets = db.session.execute(sql, {"game_id":game_id, "user_id":user_id})
    data = []
    for row in already_placed_bets:
        data.append({
            'user_id': row.user_id,
            'game_id': row.game_id
        })

    if data:
        return True

def get_bets():
    sql = text("SELECT G.home_team, G.visitor_team, G.date, U.username, B.goals_home, B.goals_visitor FROM bets B, users U, games G WHERE B.game_id=G.id AND B.user_id = U.id AND G.date BETWEEN NOW() AND G.date ORDER BY G.date")
    bets = db.session.execute(sql).fetchall()
    db.session.commit()
    return bets
       

