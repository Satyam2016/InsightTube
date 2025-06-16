# youtube-analyzer-backend/services/comment_service.py

from googleapiclient.discovery import build
from textblob import TextBlob
import os
from dotenv import load_dotenv
load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def fetch_comments(video_id: str, max_results=50):
    comments = []
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=max_results,
        textFormat="plainText"
    )
    response = request.execute()

    for item in response["items"]:
        comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        comments.append(comment)
    return comments

def analyze_comments(video_id: str) -> dict:
    comments = fetch_comments(video_id)
    sentiments = [TextBlob(c).sentiment.polarity for c in comments]

    avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
    sample_comments = comments[:5]

    return {
        "average_sentiment": avg_sentiment,
        "sample_comments": sample_comments
    }
