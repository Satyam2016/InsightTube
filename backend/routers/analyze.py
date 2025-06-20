# routers/analyze.py

from fastapi import APIRouter, HTTPException, Query
from services.transcript_service import get_transcript
from services.nlp_analysis_service import analyze_transcript
from services.comment_service import get_comments, analyze_comment_sentiments
from services.metadata_service import get_video_metadata
from services.recommendation_service import generate_recommendation
from utils.youtube_utils import extract_video_id
from utils.cache import get_from_cache, set_cache
from utils.store import store_result
from services.summary_service import summarize_transcript


router = APIRouter()


@router.get("/analyze")
def analyze_video(video_url: str = Query(..., description="YouTube video URL")):
    try:
        video_id = extract_video_id(video_url)

        # 💾 Check Cache First
        cached_result = get_from_cache(video_id)
        if cached_result:
            return {**cached_result, "cached": True}

        # 🧠 Phase 1: Transcript
        transcript = get_transcript(video_id)
        if not transcript:
            raise HTTPException(status_code=404, detail="Transcript not found")
        transcript_result = analyze_transcript(transcript)
        
        summary = summarize_transcript(transcript)

        # 💬 Phase 2: Comments
        comments = get_comments(video_id)
        comment_result = analyze_comment_sentiments(comments)

        # 🧾 Phase 3: Metadata
        metadata = get_video_metadata(video_id)

        # 💡 Phase 4: Recommendation
        recommendation = generate_recommendation(
            transcript_analysis=transcript_result,
            comment_analysis=comment_result,
            metadata=metadata
        )

        # 📦 Final Result
        result = {
            "video_id": video_id,
            "metadata": metadata,
            "transcript_analysis": transcript_result,
            "comment_analysis": comment_result,
            "recommendation": recommendation,
            "summary": summary
        }

        set_cache(video_id, result)
        store_result(result)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
