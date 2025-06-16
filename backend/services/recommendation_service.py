# youtube-analyzer-backend/services/recommendation_service.py

def generate_recommendation(transcript_data: dict, comment_data: dict) -> str:
    ts_sent = transcript_data["sentiment"]
    cm_sent = comment_data["average_sentiment"]

    if ts_sent > 0.2 and cm_sent > 0.2:
        return "This video is positively received and informative. Recommended to watch!"
    elif ts_sent < -0.2 and cm_sent < -0.2:
        return "This video has negative sentiment. Consider checking other options."
    else:
        return "Mixed feedback. Watch a portion and decide if it suits your needs."
