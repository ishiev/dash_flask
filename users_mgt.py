# from sqlalchemy import Table
from sqlalchemy.sql import select
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from config import engine
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    """ SQLalchemy model """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    actions = db.relationship('Action', backref='owner', lazy=True)

class Action(db.Model):
    """ SQLalchemy model """
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50))
    time = db.Column(db.DateTime, default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 


def create_user_table():
    Action.metadata.create_all(engine)
    User.metadata.create_all(engine)


def add_user(username, password, email):
    hashed_password = generate_password_hash(password, method='sha256')

    ins = User.insert().values(
        username=username, email=email, password=hashed_password)

    conn = engine.connect()
    conn.execute(ins)
    conn.close()


def del_user(username):
    delete = User.delete().where(User.c.username == username)

    conn = engine.connect()
    conn.execute(delete)
    conn.close()


def show_users():
    # return User.query.all()

    select_st = select([User.c.username, User.c.email])

    conn = engine.connect()
    rs = conn.execute(select_st)

    for row in rs:
        print(row)

    conn.close()
