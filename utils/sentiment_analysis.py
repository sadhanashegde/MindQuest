from textblob import TextBlob

def analyze_mood(text):
    analysis = TextBlob(text)
    sentiment = analysis.sentiment.polarity
    if sentiment > 0:
        return "Positive Mood 😊"
    elif sentiment < 0:
        return "Negative Mood 😞"
    else:
        return "Neutral Mood 😐"
