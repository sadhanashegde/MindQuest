# routes/mini_games.py
from flask import Blueprint, render_template
from flask_login import login_required

<<<<<<< HEAD
def create_mini_games_blueprint():
    mini_games_bp = Blueprint('games', __name__)

    @mini_games_bp.route('/')
    @login_required
    def games_home():
        return render_template('games/index.html')

    @mini_games_bp.route('/memory')
    @login_required
    def memory_game():
        return render_template('games/memory.html')

    @mini_games_bp.route('/puzzle')
    @login_required
    def puzzle_game():
        return render_template('games/puzzle.html')

    return mini_games_bp
=======
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
>>>>>>> 97aa00a0e4f2128dd2fca54a9cbbc5b0b5d7303a
