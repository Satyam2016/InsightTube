# youtube-analyzer-backend/services/nlp_analysis_service.py

from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from collections import Counter
import re

nltk.download('punkt')

def clean_text(text: str) -> str:
    return re.sub(r'\s+', ' ', text)

def extract_keywords(text: str, top_k=10):
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform([text])
    scores = zip(vectorizer.get_feature_names_out(), X.toarray()[0])
    return sorted(scores, key=lambda x: x[1], reverse=True)[:top_k]

def analyze_sentiment(text: str):
    return TextBlob(text).sentiment.polarity  # -1 to 1

def analyze_transcript(transcript: str) -> dict:
    cleaned = clean_text(transcript)
    sentiment = analyze_sentiment(cleaned)
    keywords = extract_keywords(cleaned)
    summary = " ".join(cleaned.split()[:50]) + "..." if len(cleaned.split()) > 50 else cleaned

    return {
        "summary": summary,
        "keywords": [kw for kw, score in keywords],
        "sentiment": sentiment
    }
