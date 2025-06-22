from pydantic import BaseModel, HttpUrl
from typing import List, Dict, Optional, Any

class VideoAnalysisRequest(BaseModel):
    video_url: str

class VideoInfo(BaseModel):
    title: str
    channel: str
    views: str
    upload_date: str
    duration: str
    likes: int
    dislikes: int
    comments: int
    description: str

class TopicAnalysis(BaseModel):
    topic: str
    relevance: float
    mentions: int

class SentimentDistribution(BaseModel):
    name: str
    value: float
    color: str

class CommentData(BaseModel):
    author: str
    text: str
    sentiment: str
    sentiment_score: float
    likes: int
    published_at: str

class CommentAnalysisDetail(BaseModel):
    total_comments: int
    avg_sentiment: float
    engagement_rate: float
    top_keywords: List[str]
    sentiment_distribution_detailed: Dict[str, int]
    emotion_distribution: Dict[str, int]
    quality_score: float

class VideoAnalysisDetail(BaseModel):
    transcript_keywords: List[str]
    transcript_emotion: str
    content_quality_score: float

class SentimentOverTime(BaseModel):
    time: str
    positive: float
    negative: float
    neutral: float

class AnalysisResponse(BaseModel):
    video_info: VideoInfo
    summary: str
    topics: List[TopicAnalysis]
    sentiment_distribution: List[SentimentDistribution]
    comment_analysis: CommentAnalysisDetail
    sentiment_over_time: List[SentimentOverTime]
    top_comments: List[CommentData]
    video_analysis_detail: VideoAnalysisDetail
    processing_time: float