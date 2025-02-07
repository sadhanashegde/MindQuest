from flask import Flask, render_template
from routes.mood_analysis import mood_bp
from routes.mini_games import games_bp
from routes.journaling import journal_bp
from routes.breathing import breathing_bp

app = Flask(__name__, static_folder="static", template_folder="templates")

# Registering Blueprints (each feature has its own route)
app.register_blueprint(mood_bp, url_prefix="/mood")
app.register_blueprint(games_bp, url_prefix="/mini-games")
app.register_blueprint(journal_bp, url_prefix="/journaling")
app.register_blueprint(breathing_bp, url_prefix="/breathing")

# Root Route (Homepage - Mood Check)
@app.route("/")
def home():
    return render_template("index.html")

# Mini-Games Route
@app.route("/mini-games")
def mini_games():
    return render_template("mini_games.html")

# Journaling Route
@app.route("/journaling")
def journaling():
    return render_template("journal.html")

# Breathing Exercise Route
@app.route("/breathing")
def breathing():
    return render_template("breathing.html")

if __name__ == "__main__":
    app.run(debug=True)
