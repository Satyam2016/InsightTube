import asyncio
from typing import List, Dict, Any, Tuple
from collections import Counter

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob

from models.schemas import (
    CommentData, SentimentDistribution, SentimentOverTime, 
    VideoAnalysisDetail
)
from services.gemini_service import GeminiService
from services.utils import clean_text, extract_keywords
from core.config import settings
from core.logger import logger

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('vader_lexicon', quiet=True)
except:
    pass

class SentimentService:
    def __init__(self):
        # Initialize NLTK components
        try:
            self.stop_words = set(stopwords.words('english'))
            self.lemmatizer = WordNetLemmatizer()
            self.sia = SentimentIntensityAnalyzer()
        except:
            self.stop_words = set()
            self.lemmatizer = None
            self.sia = None
        
        self.gemini_service = GeminiService()

    def analyze_sentiment_advanced(self, text: str) -> Tuple[str, float]:
        """Advanced sentiment analysis using multiple methods"""
        try:
            # TextBlob sentiment
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            # VADER sentiment for comparison
            if self.sia:
                vader_scores = self.sia.polarity_scores(text)
                compound = vader_scores['compound']
                
                # Combine both approaches for better accuracy
                combined_score = (polarity + compound) / 2
            else:
                combined_score = polarity
            
            if combined_score > settings.sentiment_threshold_positive:
                return "POSITIVE", combined_score
            elif combined_score < settings.sentiment_threshold_negative:
                return "NEGATIVE", combined_score
            else:
                return "NEUTRAL", combined_score
        except:
            return "NEUTRAL", 0.0

    async def analyze_comments_comprehensive(self, comments: List[CommentData]) -> Dict[str, Any]:
        """Comprehensive comment analysis using original logic with Gemini enhancement"""
        if not comments:
            return {
                "sentiment_distribution_detailed": {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0},
                "emotion_distribution": {"Neutral": 1},
                "top_keywords": []
            }
        
        # Collect all comment text for analysis
        all_text = " ".join([clean_text(comment.text) for comment in comments])
        
        # Sentiment distribution
        sentiment_counts = Counter(comment.sentiment.upper() for comment in comments)
        
        # Extract emotions using Gemini AI
        emotions = []
        for comment in comments[:20]:  # Analyze first 20 comments for emotions
            emotion = await self.gemini_service.detect_emotion_with_gemini(comment.text)
            emotions.append(emotion)
        
        emotion_counts = dict(Counter(emotions))
        
        # Extract keywords
        keywords = await self.gemini_service.extract_keywords_advanced(all_text, settings.default_keywords_count)
        if not keywords:
            keywords = extract_keywords(all_text, settings.default_keywords_count)
        
        return {
            "sentiment_distribution_detailed": dict(sentiment_counts),
            "emotion_distribution": emotion_counts,
            "top_keywords": keywords
        }

    def calculate_sentiment_distribution(self, comments: List[CommentData]) -> List[SentimentDistribution]:
        """Calculate sentiment distribution from comments"""
        if not comments:
            return [
                SentimentDistribution(name="Positive", value=60.0, color="#22c55e"),
                SentimentDistribution(name="Neutral", value=30.0, color="#64748b"),
                SentimentDistribution(name="Negative", value=10.0, color="#ef4444")
            ]
        
        sentiment_counts = Counter(comment.sentiment for comment in comments)
        total = len(comments)
        
        return [
            SentimentDistribution(
                name="Positive",
                value=round((sentiment_counts.get("positive", 0) / total) * 100, 1),
                color="#22c55e"
            ),
            SentimentDistribution(
                name="Neutral",
                value=round((sentiment_counts.get("neutral", 0) / total) * 100, 1),
                color="#64748b"
            ),
            SentimentDistribution(
                name="Negative",
                value=round((sentiment_counts.get("negative", 0) / total) * 100, 1),
                color="#ef4444"
            )
        ]

    def generate_sentiment_over_time(self, comments: List[CommentData]) -> List[SentimentOverTime]:
        """Generate sentiment analysis over time segments"""
        # For simplicity, we'll create time segments based on comment distribution
        time_segments = [
            "0-2 min", "2-4 min", "4-6 min", "6-8 min", 
            "8-10 min", "10-12 min", "12-14 min", "14+ min"
        ]
        
        sentiment_over_time = []
        segment_size = max(1, len(comments) // len(time_segments))
        
        for i, segment in enumerate(time_segments):
            start_idx = i * segment_size
            end_idx = min((i + 1) * segment_size, len(comments))
            segment_comments = comments[start_idx:end_idx]
            
            if segment_comments:
                sentiment_counts = Counter(comment.sentiment for comment in segment_comments)
                total = len(segment_comments)
                
                sentiment_over_time.append(SentimentOverTime(
                    time=segment,
                    positive=round((sentiment_counts.get("positive", 0) / total) * 100, 1),
                    negative=round((sentiment_counts.get("negative", 0) / total) * 100, 1),
                    neutral=round((sentiment_counts.get("neutral", 0) / total) * 100, 1)
                ))
            else:
                sentiment_over_time.append(SentimentOverTime(
                    time=segment,
                    positive=50.0,
                    negative=25.0,
                    neutral=25.0
                ))
        
        return sentiment_over_time

    async def analyze_transcript_comprehensive(self, transcript: str, summary: str = "", 
                                            comments_count: int = 0, engagement_rate: float = 0.0) -> VideoAnalysisDetail:
        """Comprehensive transcript analysis using original logic enhanced with Gemini"""
        try:
            # Extract keywords using advanced method
            keywords = await self.gemini_service.extract_keywords_advanced(transcript, 8)
            if not keywords:
                keywords = extract_keywords(transcript, 8)
            
            # Detect emotion using Gemini
            emotion = await self.gemini_service.detect_emotion_with_gemini(transcript)
            
            # Generate quality score using original logic
            quality_score = self.generate_video_quality_score(
                transcript, keywords, summary, comments_count, engagement_rate
            )
            
            return VideoAnalysisDetail(
                transcript_keywords=keywords,
                transcript_emotion=emotion,
                content_quality_score=quality_score
            )
        except Exception as e:
            logger.error(f"Error analyzing transcript: {e}")
            return VideoAnalysisDetail(
                transcript_keywords=[],
                transcript_emotion="Neutral",
                content_quality_score=0.5
            )

    def generate_video_quality_score(self, transcript: str, keywords: List[str], 
                                    summary: str = "", comments_count: int = 0,
                                    engagement_rate: float = 0.0) -> float:
        """Generate comprehensive video quality score"""
        score = 0.0
        
        # Content length and depth
        if len(transcript) > 2000:
            score += settings.content_length_weight
        elif len(transcript) > 1000:
            score += settings.content_length_weight * 0.6
        
        # Summary quality
        if summary and len(summary.split()) > 30:
            score += settings.summary_quality_weight
        elif summary and len(summary.split()) > 15:
            score += settings.summary_quality_weight * 0.5
        
        # Keyword richness
        if len(keywords) >= 5:
            score += settings.keyword_richness_weight
        elif len(keywords) >= 3:
            score += settings.keyword_richness_weight * 0.75
        
        # Engagement metrics
        if engagement_rate > 0.1:  # 0.1% engagement rate
            score += settings.engagement_weight
        elif engagement_rate > 0.05:
            score += settings.engagement_weight * 0.5
        
        # Comment activity
        if comments_count > 100:
            score += settings.comment_activity_weight
        elif comments_count > 50:
            score += settings.comment_activity_weight * 0.67
        
        return round(min(score, 1.0), 2)