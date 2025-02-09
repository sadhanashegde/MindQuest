from textblob import TextBlob

def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    if polarity > 0.2:
        mood = "Happy"
        points = 10
        suggestions = "Keep up the positive energy! Try journaling about your best moments."
        song_list = ["Happy - Pharrell Williams", "Good Vibes - Chris Janson"]
    elif polarity < -0.2:
        mood = "Sad"
        points = 5
        suggestions = "Try listening to music or journaling to express your emotions."
        song_list = ["Someone Like You - Adele", "Fix You - Coldplay"]
    else:
        mood = "Neutral"
        points = 3
        suggestions = "Stay mindful of your emotions. Maybe a quick game will help lift your mood?"
        song_list = ["Shape of You - Ed Sheeran", "Radioactive - Imagine Dragons"]

    stress_prediction = "Mild Stress" if polarity < -0.5 else "No significant stress detected."

    return mood, polarity, points, suggestions, song_list, stress_prediction
