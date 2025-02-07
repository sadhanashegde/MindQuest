from flask import Blueprint, render_template, request

mood_bp = Blueprint("mood", __name__)

# Function to analyze mood (Basic keyword matching for now)
def analyze_mood(text):
    text = text.lower()
    if "loneliness" in text:
        return "lonely", "/journaling"
    elif "stress" in text:
        return "stressed", "/mini-games"
    elif "anxiety" in text:
        return "anxious", "/breathing"
    else:
        return "neutral", None

@mood_bp.route("/", methods=["GET", "POST"])
def mood_check():
    mood_result = None
    activity_link = None

    if request.method == "POST":
        user_mood = request.form.get("mood_text", "")
        if not user_mood:
            mood_result = "No mood entered!"
        else:
            mood_result, activity_link = analyze_mood(user_mood)

    return render_template("index.html", mood_result=mood_result, activity_link=activity_link)