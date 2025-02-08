# routes/mini_games.py
from flask import Blueprint, render_template
from flask_login import login_required

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