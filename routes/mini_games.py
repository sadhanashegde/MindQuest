from flask import Blueprint, render_template

games_bp = Blueprint("mini_games", __name__)

@games_bp.route("/")
def mini_games():
    return render_template("mini_games.html")

@games_bp.route("/brick-breaker")
def brick_breaker():
    return render_template("brick_breaker.html")

@games_bp.route("/snake-game")
def snake_game():
    return render_template("snake_game.html")


@games_bp.route("/cross-road")
def snake_game():
    return render_template("cross_road.html")


@games_bp.route("/flappy-cube")
def snake_game():
    return render_template("flappy_cube.html")
