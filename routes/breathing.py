from flask import Blueprint, render_template
from flask_login import login_required

def create_breathing_blueprint():
    breathing_bp = Blueprint('breathing', __name__)

    @breathing_bp.route('/')
    @login_required
    def breathing_home():
        return render_template('breathing/index.html')

    @breathing_bp.route('/exercise/<exercise_type>')
    @login_required
    def breathing_exercise(exercise_type):
        return render_template('breathing/exercise.html', exercise_type=exercise_type)

    return breathing_bp
