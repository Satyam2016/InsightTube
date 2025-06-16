# youtube-analyzer-backend/services/metadata_service.py

from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")  # Set this in your .env or environment
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def fetch_metadata(video_id: str) -> dict:
    response = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        id=video_id
    ).execute()

    if not response["items"]:
        raise ValueError("Video not found.")

    item = response["items"][0]
    snippet = item["snippet"]
    stats = item["statistics"]

    return {
        "title": snippet["title"],
        "channel": snippet["channelTitle"],
        "description": snippet["description"],
        "published_at": snippet["publishedAt"],
        "views": stats.get("viewCount", "0"),
        "likes": stats.get("likeCount", "0"),
        "comments": stats.get("commentCount", "0"),
        "tags": snippet.get("tags", [])
    }
