from flask import Flask
from routes.mood_analysis import mood_bp
from routes.mini_games import games_bp
from routes.journaling import journal_bp
from routes.breathing import breathing_bp

app = Flask(__name__)

# Registering blueprints
app.register_blueprint(mood_bp)
app.register_blueprint(games_bp)
app.register_blueprint(journal_bp)
app.register_blueprint(breathing_bp)

if __name__ == "__main__":
    app.run(debug=True)
