import re
from datetime import datetime
from typing import List
from fastapi import HTTPException
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_transcript_api import YouTubeTranscriptApi

from models.schemas import VideoInfo, CommentData
from services.sentiment_service import SentimentService
from services.utils import clean_text
from core.config import settings
from core.logger import logger

class YouTubeService:
    def __init__(self):
        self.youtube = build('youtube', 'v3', developerKey=settings.youtube_api_key)
        self.sentiment_service = SentimentService()

    async def get_video_info_enhanced(self, video_id: str) -> VideoInfo:
        """Enhanced video information fetching with metadata"""
        try:
            request = self.youtube.videos().list(
                part="snippet,statistics,contentDetails",
                id=video_id
            )
            response = request.execute()
            
            if not response['items']:
                raise HTTPException(status_code=404, detail="Video not found")
            
            video = response['items'][0]
            snippet = video['snippet']
            statistics = video['statistics']
            content_details = video['contentDetails']
            
            # Parse duration
            duration = content_details['duration']
            duration_match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration)
            if duration_match:
                hours = int(duration_match.group(1) or 0)
                minutes = int(duration_match.group(2) or 0)
                seconds = int(duration_match.group(3) or 0)
                duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}" if hours else f"{minutes:02d}:{seconds:02d}"
            else:
                duration_str = "00:00"
            
            # Format upload date
            upload_date = datetime.fromisoformat(snippet['publishedAt'].replace('Z', '+00:00'))
            days_ago = (datetime.now().replace(tzinfo=upload_date.tzinfo) - upload_date).days
            upload_date_str = f"{days_ago} days ago" if days_ago > 0 else "Today"
            
            # Format view count
            view_count = int(statistics.get('viewCount', 0))
            if view_count >= 1000000:
                views_str = f"{view_count/1000000:.1f}M views"
            elif view_count >= 1000:
                views_str = f"{view_count/1000:.1f}K views"
            else:
                views_str = f"{view_count} views"
            
            return VideoInfo(
                title=snippet['title'],
                channel=snippet['channelTitle'],
                views=views_str,
                upload_date=upload_date_str,
                duration=duration_str,
                likes=int(statistics.get('likeCount', 0)),
                dislikes=int(statistics.get('dislikeCount', 0)),
                comments=int(statistics.get('commentCount', 0)),
                description=snippet.get('description', '')
            )
        except HttpError as e:
            logger.error(f"YouTube API error: {e}")
            raise HTTPException(status_code=400, detail="Error fetching video information")

    async def get_video_comments(self, video_id: str, max_results: int = 100) -> List[CommentData]:
        """Fetch video comments from YouTube API with enhanced analysis"""
        comments = []
        try:
            request = self.youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=min(max_results, settings.max_comments),
                order="relevance",
                textFormat="plainText"
            )
            response = request.execute()
            
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                text = clean_text(comment['textDisplay'])
                sentiment, score = self.sentiment_service.analyze_sentiment_advanced(text)
                
                comments.append(CommentData(
                    author=comment['authorDisplayName'],
                    text=comment['textDisplay'],
                    sentiment=sentiment.lower(),
                    sentiment_score=score,
                    likes=comment.get('likeCount', 0),
                    published_at=comment['publishedAt']
                ))
                
        except HttpError as e:
            logger.error(f"Error fetching comments: {e}")
        
        return comments

    async def get_video_transcript(self, video_id: str) -> str:
        """Get video transcript using youtube-transcript-api"""
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            return ' '.join([entry['text'] for entry in transcript])
        except:
            logger.warning(f"Could not fetch transcript for video {video_id}")
            return ""

    def calculate_engagement_rate(self, comments: List[CommentData], views_str: str) -> float:
        """Calculate engagement rate based on comments and views"""
        try:
            # Parse view count from string
            view_count = int(views_str.split()[0].replace('M', '000000').replace('K', '000').replace(',', ''))
            engagement_rate = (len(comments) / max(1, view_count)) * 100
            return engagement_rate
        except:
            return 0.0