from flask import Blueprint, render_template

games_bp = Blueprint("games", __name__)

@games_bp.route("/mini-games")
def mini_games():
    return render_template("mini_games.html")
