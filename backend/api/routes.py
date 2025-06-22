from fastapi import APIRouter, HTTPException # type: ignore
from datetime import datetime
import statistics

from models.schemas import VideoAnalysisRequest, AnalysisResponse, CommentAnalysisDetail
from services.youtube_service import YouTubeService
from services.gemini_service import GeminiService
from services.sentiment_service import SentimentService
from services.utils import extract_video_id
from core.logger import logger

router = APIRouter()

# Initialize services
youtube_service = YouTubeService()
gemini_service = GeminiService()
sentiment_service = SentimentService()

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_video(request: VideoAnalysisRequest):
    """Analyze a YouTube video"""
    start_time = datetime.now()
    
    try:
        # Extract video ID
        video_id = extract_video_id(request.video_url)
        
        # Fetch video information
        video_info = await youtube_service.get_video_info_enhanced(video_id)
        
        # Fetch comments
        comments = await youtube_service.get_video_comments(video_id, max_results=100)
        
        # Get transcript
        transcript = await youtube_service.get_video_transcript(video_id)
        
        # Generate summary
        summary = await gemini_service.generate_summary(transcript, video_info.description)
        
        # Extract topics
        topics = await gemini_service.extract_topics(transcript, video_info.description)
        
        # Comprehensive comment analysis
        comment_analysis_data = await sentiment_service.analyze_comments_comprehensive(comments)
        
        # Calculate sentiment distribution
        sentiment_distribution = sentiment_service.calculate_sentiment_distribution(comments)
        
        # Generate sentiment over time
        sentiment_over_time = sentiment_service.generate_sentiment_over_time(comments)
        
        # Comprehensive transcript analysis
        engagement_rate = youtube_service.calculate_engagement_rate(comments, video_info.views)
        video_analysis = await sentiment_service.analyze_transcript_comprehensive(
            transcript, summary, len(comments), engagement_rate
        )
        
        # Prepare detailed comment analysis
        sentiment_scores = [comment.sentiment_score for comment in comments if comment.sentiment_score != 0]
        avg_sentiment = statistics.mean(sentiment_scores) if sentiment_scores else 0.0
        
        comment_analysis = CommentAnalysisDetail(
            total_comments=len(comments),
            avg_sentiment=round(avg_sentiment, 2),
            engagement_rate=round(engagement_rate, 2),
            top_keywords=comment_analysis_data["top_keywords"],
            sentiment_distribution_detailed=comment_analysis_data["sentiment_distribution_detailed"],
            emotion_distribution=comment_analysis_data["emotion_distribution"],
            quality_score=video_analysis.content_quality_score
        )
        
        # Get top comments
        top_comments = sorted(comments, key=lambda x: x.likes, reverse=True)[:5]
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return AnalysisResponse(
            video_info=video_info,
            summary=summary,
            topics=topics,
            sentiment_distribution=sentiment_distribution,
            comment_analysis=comment_analysis,
            sentiment_over_time=sentiment_over_time,
            top_comments=top_comments,
            video_analysis_detail=video_analysis,
            processing_time=round(processing_time, 2)
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during analysis")