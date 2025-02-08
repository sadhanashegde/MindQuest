from flask import Flask, Blueprint, render_template, request, render_template_string
from textblob import TextBlob
import json
from collections import deque
import statistics

app = Flask(__name__)

affirmations = []
MOOD_WINDOW_SIZE = 5
mood_history = deque(maxlen=MOOD_WINDOW_SIZE)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MindQuest Advanced Emotion Analysis</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: {{ background_color }};
            text-align: center;
            padding: 30px;
        }
        .result {
            background-color: #e0f7fa;
            padding: 15px;
            border-radius: 8px;
            display: inline-block;
            margin-top: 20px;
        }
        .positive { color: green; }
        .negative { color: red; }
        .neutral { color: gray; }
        textarea { width: 80%; height: 100px; }
        button { padding: 10px 20px; background-color: #00796b; color: white; border: none; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>MindQuest: AI-Driven Emotion Analysis & Prediction</h1>

    <!-- Emotion Analysis Form -->
    <h3>Analyze Your Mood</h3>
    <form method="POST" action="/">
        <textarea id="text_input" name="text_input" placeholder="Type your thoughts here..."></textarea><br><br>
        <button type="submit">Analyze Emotion</button>
    </form>

    {% if result %}
    <div class="result">
        <h2>Emotion Result:</h2>
        <p class="{{ emotion_class }}">{{ result }}</p>
        <p>Polarity Score: {{ polarity }}</p>
        <p>You earned {{ points }} self-care points!</p>
        <p><strong>Suggestions:</strong> {{ suggestions }}</p>
        {% if activity_link %}
        <p><a href="{{ activity_link }}">Click here for your recommended activity.</a></p>
        {% endif %}
        {% if stress_prediction %}
        <p><strong>Prediction:</strong> {{ stress_prediction }}</p>
        {% endif %}
    </div>
    {% endif %}

    <!-- Affirmation Form -->
    <h3>Share a Positive Affirmation</h3>
    <form method="POST" action="/affirmations">
        <textarea name="affirmation" placeholder="Share an affirmation..."></textarea><br><br>
        <button type="submit">Post Affirmation</button>
    </form>

    <h3>Affirmation Wall</h3>
    <div>
        {% for affirmation in affirmations %}
            <p>🌟 {{ affirmation }}</p>
        {% endfor %}
    </div>
</body>
</html>
"""

# Analyze mood with more specific categorization
def analyze_mood(text):
    text = text.lower()
    if "lonely" in text or "loneliness" in text:
        return "lonely", "/journaling", "How about expressing your feelings in a journal?"
    elif "stress" in text or "stressed" in text:
        return "stressed", "/mini-games", "Try some fun mini-games to relax."
    elif "anxiety" in text or "anxious" in text:
        return "anxious", "/breathing", "Take a 5-minute breathing exercise to calm down."
    else:
        return "negative", "/mini-games", "Try some fun mini-games as a general pick-me-up."

@app.route("/", methods=["GET", "POST"])
def analyze_text_emotion():
    result = None
    emotion_class = "neutral"
    polarity = 0
    points = 0
    suggestions = None
    activity_link = None
    background_color = "#f0f0f0"  # Default background color for neutral
    stress_prediction = None

    if request.method == "POST":
        user_text = request.form.get("text_input")

        if user_text:
            # Analyze emotion using TextBlob
            analysis = TextBlob(user_text)
            polarity = analysis.sentiment.polarity

            # Determine sentiment category and points
            if polarity > 0:
                result = "Positive Emotion 😊"
                emotion_class = "positive"
                points = 10
                suggestions = "Keep up the positivity! How about a creative journaling challenge?"
                background_color = "#ccffcc"  # Light green for positivity
            elif polarity < 0:
                mood_result, activity_link, suggestions = analyze_mood(user_text)
                result = f"Negative Emotion ({mood_result.capitalize()}) 😢"
                emotion_class = "negative"
                points = 5
                background_color = "#ffcccc"  # Light red for negativity
            else:
                result = "Neutral Emotion 😐"
                emotion_class = "neutral"
                points = 7
                suggestions = "Feeling neutral? Maybe explore a mindfulness activity."
                background_color = "#f0f0f0"  # Light gray for neutral

            # Save mood data and update mood history for predictive analytics
            save_mood_data(user_text, polarity)
            mood_history.append(polarity)

            # Predict potential stress based on historical polarity data
            if len(mood_history) == MOOD_WINDOW_SIZE:
                average_mood = statistics.mean(mood_history)
                if average_mood < -0.1:
                    stress_prediction = "Potential stress or anxiety detected. Consider a guided breathing exercise or a calming activity."
                elif average_mood > 0.2:
                    stress_prediction = "Your mood trend is positive! Keep it up with creative journaling."

    return render_template_string(
        HTML_TEMPLATE, result=result, polarity=polarity,
        emotion_class=emotion_class, points=points, suggestions=suggestions,
        affirmations=affirmations, background_color=background_color,
        stress_prediction=stress_prediction, activity_link=activity_link
    )

@app.route("/affirmations", methods=["POST"])
def handle_affirmations():
    affirmation = request.form.get("affirmation")
    if affirmation:
        affirmations.append(affirmation)
    return analyze_text_emotion()

@app.route("/journaling")
def journaling():
    return "<h1>Welcome to the Journaling Page</h1>"

@app.route("/mini-games")
def mini_games():
    return "<h1>Welcome to the Mini-Games Page</h1>"

@app.route("/breathing")
def breathing():
    return "<h1>Welcome to the Breathing Exercises Page</h1>"

# Save mood data to a JSON file
def save_mood_data(text, polarity):
    mood_entry = {"text": text, "polarity": polarity}
    with open("mood_data.json", "a") as file:
        json.dump(mood_entry, file)
        file.write("\n")

if __name__ == "__main__":
    app.run(debug=True)
