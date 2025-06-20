from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
load_dotenv()
# Replace with your actual YouTube Data API key
API_KEY =  os.getenv("YOUTUBE_API_KEY")

def get_video_metadata(video_id: str) -> dict:
    youtube = build("youtube", "v3", developerKey=API_KEY)
    request = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        id=video_id
    )
    response = request.execute()

    if not response["items"]:
        return {}

    item = response["items"][0]
    snippet = item["snippet"]
    stats = item["statistics"]
    content = item["contentDetails"]

    return {
        "title": snippet.get("title"),
        "description": snippet.get("description"),
        "channel_title": snippet.get("channelTitle"),
        "published_at": snippet.get("publishedAt"),
        "duration": content.get("duration"),
        "view_count": stats.get("viewCount"),
        "like_count": stats.get("likeCount"),
        "comment_count": stats.get("commentCount"),
        "tags": snippet.get("tags", [])
    }
