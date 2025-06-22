import re
from typing import List
from collections import Counter

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from core.config import settings

# Initialize NLTK components
try:
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
except:
    stop_words = set()
    lemmatizer = None

def extract_video_id(url: str) -> str:
    """Extract YouTube video ID from URL"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        r'youtube\.com\/watch\?.*v=([^&\n?#]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    raise ValueError("Invalid YouTube URL")

def clean_text(text: str) -> str:
    """Clean text by removing URLs, mentions, and extra whitespace"""
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[@#]\w+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text.lower()

def extract_keywords(text: str, num_keywords: int = 10) -> List[str]:
    """Extract keywords from text using NLTK"""
    try:
        if not lemmatizer:
            return []
            
        tokens = word_tokenize(text.lower())
        tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalpha()]
        tokens = [token for token in tokens if token not in stop_words and len(token) > 2]
        
        word_freq = Counter(tokens)
        return [word for word, freq in word_freq.most_common(num_keywords)]
    except:
        return []

def format_view_count(view_count: int) -> str:
    """Format view count into readable string"""
    if view_count >= 1000000:
        return f"{view_count/1000000:.1f}M views"
    elif view_count >= 1000:
        return f"{view_count/1000:.1f}K views"
    else:
        return f"{view_count} views"

def parse_duration(duration: str) -> str:
    """Parse ISO 8601 duration to readable format"""
    duration_match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration)
    if duration_match:
        hours = int(duration_match.group(1) or 0)
        minutes = int(duration_match.group(2) or 0)
        seconds = int(duration_match.group(3) or 0)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}" if hours else f"{minutes:02d}:{seconds:02d}"
    else:
        return "00:00"

def calculate_days_ago(published_at: str) -> str:
    """Calculate days ago from published date"""
    from datetime import datetime
    
    upload_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
    days_ago = (datetime.now().replace(tzinfo=upload_date.tzinfo) - upload_date).days
    return f"{days_ago} days ago" if days_ago > 0 else "Today"