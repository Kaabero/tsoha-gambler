from datetime import datetime
from sqlalchemy.sql import text
from db import db

def bet(game_id, user_id, goals_home, goals_visitor):

    sql = text("SELECT date FROM games WHERE id=:game_id")
    date = db.session.execute(sql, {'game_id': game_id})

    for row in date:
        if row.date > datetime.now():

            try:
                sql = text(
                    """INSERT INTO bets (game_id, user_id, goals_home, goals_visitor)
                       VALUES (:game_id, :user_id, :goals_home, :goals_visitor)""")
                db.session.execute(sql,
                                   {"game_id": game_id,
                                    "user_id": user_id,
                                    "goals_home": goals_home,
                                    "goals_visitor": goals_visitor})
                db.session.commit()
                return True
            except BaseException:
                return False

    return False


def already_placed_bet(user_id, game_id):

    sql = text(
        "SELECT user_id, game_id FROM bets WHERE game_id=:game_id AND user_id=:user_id")
    already_placed_bets = db.session.execute(
        sql, {"game_id": game_id, "user_id": user_id})
    data = []
    for row in already_placed_bets:
        data.append({
            'user_id': row.user_id,
            'game_id': row.game_id
        })

    return data

def get_bets():
    sql = text(
        """SELECT G.home_team, G.visitor_team, G.date, U.username, B.goals_home, B.goals_visitor
                  FROM bets B, users U, games G
                  WHERE B.game_id=G.id AND B.user_id = U.id 
                  ORDER BY G.date DESC""")
    bets = db.session.execute(sql).fetchall()
    return bets


def own_bets(user_id):
    sql = text(
        """SELECT B.game_id, G.home_team, G.visitor_team, G.date, B.goals_home, B.goals_visitor
                  FROM bets B, games G
                  WHERE G.id=B.game_id AND user_id=:user_id AND G.date BETWEEN NOW() 
                  AND G.date ORDER BY G.date""")
    bets = db.session.execute(sql, {"user_id": user_id}).fetchall()
    return bets


def delete_bet(user_id, game_id):

    sql = text(
        """SELECT date FROM games G, bets B
        WHERE B.game_id = G.id AND B.game_id=:game_id AND B.user_id=:user_id""")
    date = db.session.execute(sql, {"game_id": game_id, "user_id": user_id})

    for row in date:
        if row.date > datetime.now():
            try:
                sql = text(
                    "DELETE FROM bets WHERE game_id=:game_id AND user_id=:user_id")
                db.session.execute(
                    sql, {"user_id": user_id, "game_id": game_id})
                db.session.commit()
                return True
            except BaseException:
                return False
        else:
            return False
    return False
