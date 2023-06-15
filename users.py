from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from db import db


def login(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        return False
    if check_password_hash(user.password, password):
        session["user_id"] = user.id
        return True

    return False


def logout():
    del session["user_id"]


def register(username, password):
    hash_value = generate_password_hash(password)

    try:
        sql = text(
            "INSERT INTO users (username,password) VALUES (:username,:password)")
        db.session.execute(sql, {"username": username, "password": hash_value})
        db.session.commit()
    except BaseException:
        return False
    return login(username, password)


def too_short_password(password):
    return len(password) < 8 or len(password) > 30


def too_short_username(username):
    return 31 > len(username) < 2 or len(username) > 30

def user_id():
    return session.get("user_id", 0)

def is_admin():
    return True
