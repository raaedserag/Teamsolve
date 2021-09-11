from random import random, choice

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .models import User, Team, Problem
from time import time
from .auth import encrypt_id

views = Blueprint("views", __name__)


@views.route('/', methods=["GET", "POST"])
@login_required
def home():
    team = Team.query.filter_by(id=current_user.teamId).first()

    if team and not current_user.solvedTodayIndices:
        lst = ['0' for i in range(get_team().problemsNum)]
        current_user.solvedTodayIndices = "".join(lst)
        db.session.commit()

    if not team:
        problemset = []
        team = Team(name="", problemsNum=0, index=0, members=[], listNum=0, id=9999)

    else:
        problemset = get_today_problems()

    team_mates = get_team_mates()
    team_mates = sorted(team_mates, key=lambda x: x.solvedToday, reverse=True)

    colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c']

    while len(colors) < len(team_mates):
        colors += colors

    return render_template("home.html", user=current_user, team=team, problemset=problemset,
                           code=encrypt_id(team.id), team_mates=team_mates, colors=colors)


@views.route('/solved')
@login_required
def solved():
    problemIndex = int(request.args.get('num'))
    st = current_user.solvedTodayIndices
    if problemIndex >= len(st):
        return home()
    lst = list(st)
    if lst[problemIndex] != '1':
        lst[problemIndex] = '1'
        current_user.solvedTodayIndices = "".join(lst)
        current_user.solvedToday += 1
        db.session.commit()

    return redirect(url_for('views.home'))


def get_team():
    return Team.query.get(current_user.teamId)


def get_problem_name(id):
    return Problem.query.get(id).name


def get_problems_start_index(team):
    return team.index


def get_problems_number(team):
    return team.problemsNum


def get_today_problems():
    team = get_team()
    start = get_problems_start_index(team)
    end = start + get_problems_number(team)
    return [get_problem_name(i+1) for i in range(start, end)]


def get_team_mates():
    teamMates = list(User.query.filter_by(teamId=current_user.teamId))
    teamMates.remove(current_user)
    return teamMates


