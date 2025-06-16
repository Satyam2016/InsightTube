# routers/analyze.py

from fastapi import APIRouter, Query
from services import (
    metadata_service,
    transcript_service,
    nlp_analysis_service,
    comment_service,
    recommendation_service
)
from models.analysis_result import FullAnalysisResponse

router = APIRouter()

@router.get("/analyze", response_model=FullAnalysisResponse)
def analyze(video_url: str = Query(..., description="Full YouTube video URL")):
    from utils.youtube_utils import extract_video_id

    vid = extract_video_id(video_url)
    
    metadata = metadata_service.fetch_metadata(vid)
    transcript = transcript_service.fetch_transcript(vid)
    transcript_analysis = nlp_analysis_service.analyze_transcript(transcript)
    comment_analysis = comment_service.analyze_comments(vid)
    recommendation = recommendation_service.generate_recommendation(transcript_analysis, comment_analysis)

    return {
        "video_metadata": metadata,
        "transcript_analysis": transcript_analysis,
        "comment_insights": comment_analysis,
        "final_recommendation": recommendation
    }
