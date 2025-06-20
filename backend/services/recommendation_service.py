# services/recommendation_service.py

def generate_recommendation(transcript_analysis: dict, comment_analysis: dict, metadata: dict) -> dict:
    sentiment = comment_analysis["sentiment_breakdown"]
    emotion_score = transcript_analysis.get("emotion_score", 0.5)
    view_count = int(metadata.get("view_count", 0))
    like_count = int(metadata.get("like_count", 0))
    comment_count = int(metadata.get("comment_count", 0))

    total_sentiment = sentiment["positive"] + sentiment["neutral"] + sentiment["negative"]
    positive_ratio = sentiment["positive"] / total_sentiment if total_sentiment else 0

    # Viewer Recommendation
    if positive_ratio >= 0.6 and emotion_score >= 0.6:
        viewer_tip = "Highly Recommended to Watch"
    elif positive_ratio >= 0.4:
        viewer_tip = "Consider Watching Based on Your Interest"
    else:
        viewer_tip = "May Skip – Mixed/Negative Feedback"

    # Creator Suggestions
    suggestions = []
    if positive_ratio < 0.5:
        suggestions.append("Improve content clarity or engagement to reduce negative sentiment.")
    if emotion_score < 0.4:
        suggestions.append("Add emotional hooks or storytelling to make content more engaging.")
    if view_count < 1000:
        suggestions.append("Boost visibility through SEO or social media.")
    if comment_count < 10:
        suggestions.append("Encourage viewers to engage in comments.")

    return {
        "viewer_tip": viewer_tip,
        "creator_suggestions": suggestions
    }
