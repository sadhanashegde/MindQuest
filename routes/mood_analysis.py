from flask import Blueprint, render_template, request
from utils.sentiment_analysis import analyze_mood

mood_bp = Blueprint("mood", __name__)

@mood_bp.route("/", methods=["GET", "POST"])
def home():
    mood_result = None
    if request.method == "POST":
        user_input = request.form["mood_text"]
        mood_result = analyze_mood(user_input)
    return render_template("index.html", mood_result=mood_result)
