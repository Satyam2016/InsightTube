from pydantic import BaseModel
from typing import List, Optional

class TranscriptAnalysis(BaseModel):
    summary: str
    keywords: List[str]
    dominant_emotion: str
    quality_score: float

# Replace in FullAnalysisResponse
class FullAnalysisResponse(BaseModel):
    video_metadata: dict
    transcript_analysis: TranscriptAnalysis
    comment_insights: dict
    final_recommendation: str
