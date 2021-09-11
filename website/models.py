from . import db
from flask_login import UserMixin


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    problemsNum = db.Column(db.Integer)
    index = db.Column(db.Integer)
    listNum = db.Column(db.Integer)
    members = db.relationship('User')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    solvedToday = db.Column(db.Integer)
    solvedTodayIndices = db.Column(db.String(200))
    solvedOverall = db.Column(db.Integer)
    teamId = db.Column(db.Integer, db.ForeignKey('team.id'))

    def resetDailySolved(self):
        self.solvedToday = 0
        self.solvedTodayIndices = '[]'


class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(7))

