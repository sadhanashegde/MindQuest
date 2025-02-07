from flask import Blueprint, render_template

breathing_bp = Blueprint("breathing", __name__)

@breathing_bp.route("/breathing")
def breathing():
    return render_template("breathing.html")
