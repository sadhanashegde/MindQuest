from flask import Flask, request, render_template_string
from textblob import TextBlob

app = Flask(__name__)

# HTML Template for Rendering
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Emotion Analysis Result</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f9;
            text-align: center;
            padding: 50px;
        }
        .result {
            background-color: #e0f7fa;
            padding: 20px;
            border-radius: 10px;
            display: inline-block;
            margin-top: 30px;
        }
        .positive { color: green; }
        .negative { color: red; }
        .neutral { color: gray; }
    </style>
</head>
<body>
    <h1>Emotion Analysis of Text</h1>
    <form method="POST" action="/">
        <label for="text_input">Enter your text:</label><br><br>
        <textarea id="text_input" name="text_input" rows="5" cols="50" placeholder="Type your text here..."></textarea><br><br>
        <button type="submit">Analyze Emotion</button>
    </form>

    {% if result %}
    <div class="result">
        <h2>Emotion Result:</h2>
        <p class="{{ emotion_class }}">{{ result }}</p>
        <p>Polarity Score: {{ polarity }}</p>
    </div>
    {% endif %}
</body>
</html>
"""

# Route to handle emotion analysis
@app.route("/", methods=["GET", "POST"])
def analyze_text_emotion():
    result = None
    emotion_class = "neutral"
    polarity = 0

    if request.method == "POST":
        user_text = request.form.get("text_input")
        
        if user_text:
            # Analyze emotion using TextBlob
            analysis = TextBlob(user_text)
            polarity = analysis.sentiment.polarity
            
            # Determine sentiment category
            if polarity > 0:
                result = "Positive Emotion 😊"
                emotion_class = "positive"
            elif polarity < 0:
                result = "Negative Emotion 😢"
                emotion_class = "negative"
            else:
                result = "Neutral Emotion 😐"
                emotion_class = "neutral"
    
    return render_template_string(HTML_TEMPLATE, result=result, polarity=polarity, emotion_class=emotion_class)


if __name__ == "__main__":
    app.run(debug=True)
