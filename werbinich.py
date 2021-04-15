#!/usr/bin/python3
from flask import Flask, render_template, request, url_for, redirect
from pprint import pprint
from uuid import uuid4

app = Flask(__name__)
games = {}

@app.route("/")
def new_game():
    return render_template("new_game.html")

@app.route("/", methods=["post"])
def create_game():
    global games
    pnames = [ x for x in request.form.getlist("pname") if x != "" ]
    gameid = str(uuid4())
    mapping = {}
    for player in pnames:
        mapping[player] = None
    games[gameid] = mapping

    return redirect(url_for("player_select", gameid=gameid), 303)

@app.route("/game/<uuid:gameid>/")
def player_select(gameid):
    return render_template("player_select.html", players=games[str(gameid)].keys(), gameurl=url_for("player_select", gameid=gameid))

@app.route("/game/<uuid:gameid>/edit/<player>")
def name_edit(gameid, player):
    all_players = games[str(gameid)].keys()
    other_players = [ x for x in all_players if x != player ]
    return render_template("name_edit.html", current_player=player, other_players=other_players)
    
@app.route("/game/<uuid:gameid>/edit/<player>", methods=["post"])
def store_name(gameid, player):
    all_players = games[str(gameid)].keys()
    for p in all_players:
        if p not in request.form:
            continue
        if request.form[p]:
            games[str(gameid)][p] = request.form[p]
    return redirect(url_for("name_show", gameid=gameid, player=player), 303)

@app.route("/game/<uuid:gameid>/show/<player>")
def name_show(gameid, player):
    other_players = dict(games[str(gameid)])
    other_players.pop(player, None)
    return render_template("name_show.html", current_player=player, other_players=other_players, edit_url=url_for("name_edit", gameid=gameid, player=player))

@app.errorhandler(KeyError)
def not_found(error):
    return render_template("not_found.html"), 404
