from sqlalchemy.sql import text
from db import db


def add_scores(game_id, goals_home, goals_visitor):

    correct_bets = get_correct_bets(game_id, goals_home, goals_visitor)
    for user in correct_bets:
        add_three_points(game_id, user)

    if goals_home > goals_visitor:
        correct_home_wins = home_wins(game_id)
        block_double_points(correct_bets, correct_home_wins, game_id)

    elif goals_home < goals_visitor:
        correct_visitor_wins = visitor_wins(game_id)
        block_double_points(correct_bets, correct_visitor_wins, game_id)

    else:
        correct_draw = draw(game_id)
        block_double_points(correct_bets, correct_draw, game_id)


def get_correct_bets(game_id, goals_home, goals_visitor):
    sql = text(
        """SELECT user_id FROM bets
           WHERE game_id=:game_id
           AND goals_home=:goals_home
           AND goals_visitor=:goals_visitor""")
    users = db.session.execute(sql,
                               {"game_id": game_id,
                                "goals_home": goals_home,
                                "goals_visitor": goals_visitor}).fetchall()

    bets = []

    for user in users:
        bets.append(user[0])

    return bets


def home_wins(game_id):
    sql = text(
        "SELECT user_id FROM bets WHERE goals_home > goals_visitor AND game_id=:game_id")
    users = db.session.execute(sql, {"game_id": game_id}).fetchall()

    correct_home_wins = []

    for user in users:
        correct_home_wins.append(user[0])

    return correct_home_wins


def visitor_wins(game_id):
    sql = text(
        "SELECT user_id FROM bets WHERE goals_home < goals_visitor AND game_id=:game_id")
    users = db.session.execute(sql, {"game_id": game_id}).fetchall()

    correct_visitor_wins = []

    for user in users:
        correct_visitor_wins.append(user[0])

    return correct_visitor_wins


def draw(game_id):
    sql = text(
        "SELECT user_id FROM bets WHERE goals_home = goals_visitor AND game_id=:game_id")
    users = db.session.execute(sql, {"game_id": game_id}).fetchall()

    correct_draw = []

    for user in users:
        correct_draw.append(user[0])

    return correct_draw


def add_three_points(game_id, user_id):
    sql = text(
        "INSERT INTO scores (game_id, user_id, scores) VALUES (:game_id, :user_id, :scores)")
    db.session.execute(
        sql, {"game_id": game_id, "user_id": user_id, "scores": 3})
    db.session.commit()


def add_one_point(game_id, user_id):
    sql = text(
        "INSERT INTO scores (game_id, user_id, scores) VALUES (:game_id, :user_id, :scores)")
    db.session.execute(
        sql, {"game_id": game_id, "user_id": user_id, "scores": 1})
    db.session.commit()


def get_scores():
    sql = text("""SELECT G.home_team, G.visitor_team, G.date,
                  S.scores, U.username, B.goals_home, B.goals_visitor,
                  O.goals_home as outcome_home, O.goals_visitor as outcome_visitor
                  FROM bets B, outcomes O, scores S, users U, games G
                  WHERE S.user_id=U.id AND S.game_id=G.id
                  AND O.game_id=G.id AND B.game_id=G.id AND B.user_id = U.id
                  ORDER BY G.date""")
    scores = db.session.execute(sql).fetchall()
    return scores


def get_total_scores():
    sql = text("""SELECT SUM(S.scores) as total_scores, U.username
                  FROM scores S RIGHT JOIN users U ON S.user_id=U.id GROUP BY U.username""")
    scores = db.session.execute(sql).fetchall()
    return scores


def block_double_points(correctly_betted, correct_winner, game_id):

    for user in correct_winner:
        if user not in correctly_betted:
            add_one_point(game_id, user)
