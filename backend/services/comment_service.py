# services/comment_service.py
from youtube_transcript_api._errors import TranscriptsDisabled
from googleapiclient.discovery import build
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon')
from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")  # Replace with your actual API key

def get_comments(video_id: str, max_results: int = 50) -> list:
    youtube = build("youtube", "v3", developerKey=API_KEY)
    comments = []

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=max_results,
        textFormat="plainText"
    )
    response = request.execute()

    for item in response.get("items", []):
        comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        comments.append(comment)

    return comments

def analyze_comment_sentiments(comments: list) -> dict:
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = {"positive": 0, "neutral": 0, "negative": 0}

    for comment in comments:
        score = sia.polarity_scores(comment)
        if score["compound"] >= 0.5:
            sentiment_scores["positive"] += 1
        elif score["compound"] <= -0.5:
            sentiment_scores["negative"] += 1
        else:
            sentiment_scores["neutral"] += 1

    total = sum(sentiment_scores.values()) or 1  # Avoid divide-by-zero
    sentiment_percentages = {
        k: round((v / total) * 100, 2) for k, v in sentiment_scores.items()
    }

    return {
        "total_comments_analyzed": total,
        "sentiment_breakdown": sentiment_percentages
    }
