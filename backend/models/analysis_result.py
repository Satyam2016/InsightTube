# youtube-analyzer-backend/models/analysis_result.py

from pydantic import BaseModel
from typing import List

class TranscriptAnalysis(BaseModel):
    summary: str
    keywords: List[str]
    sentiment: float

class CommentAnalysis(BaseModel):
    average_sentiment: float
    sample_comments: List[str]

class Metadata(BaseModel):
    title: str
    channel: str
    views: str
    likes: str
    description: str
    published_at: str
    tags: List[str]

class FullAnalysisResponse(BaseModel):
    video_metadata: Metadata
    transcript_analysis: TranscriptAnalysis
    comment_insights: CommentAnalysis
    final_recommendation: str
