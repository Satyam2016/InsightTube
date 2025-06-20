# routers/dashboard.py

from fastapi import APIRouter
from utils.store import get_all_results
from collections import Counter
import isodate

router = APIRouter()

@router.get("/dashboard/stats")
def get_dashboard_stats():
    results = get_all_results()

    tag_counter = Counter()
    sentiment_counter = Counter()
    total_duration = 0
    total_videos = len(results)

    for r in results:
        # Tags
        tags = r["metadata"].get("tags", [])
        tag_counter.update(tags)

        # Sentiments
        sentiments = r["comment_analysis"]["sentiment_breakdown"]
        sentiment_counter.update(sentiments)

        # Duration
        iso_duration = r["metadata"].get("duration")
        if iso_duration:
            try:
                duration = isodate.parse_duration(iso_duration).total_seconds()
                total_duration += duration
            except:
                pass

    return {
        "total_videos_analyzed": total_videos,
        "most_common_tags": tag_counter.most_common(10),
        "sentiment_summary": dict(sentiment_counter),
        "average_duration_minutes": round(total_duration / 60 / total_videos, 2) if total_videos else 0
    }
