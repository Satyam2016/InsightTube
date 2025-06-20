# services/nlp_analysis_service.py
from keybert import KeyBERT
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk


# Initialize models
kw_model = KeyBERT()
sia = SentimentIntensityAnalyzer()

# Ensure punkt tokenizer is available
nltk.download('punkt_tab', quiet=True)

def summarize_transcript(transcript_text: str, sentence_count: int = 3) -> str:
    if not transcript_text or len(transcript_text.strip()) == 0:
        return "Transcript text is empty or unavailable."

    try:
      
        parser = PlaintextParser.from_string(transcript_text, Tokenizer("english"))
     
        summarizer = TextRankSummarizer()
      
        summary = summarizer(parser.document, sentence_count)
 
        return " ".join(str(sentence) for sentence in summary)
    
    except Exception as e:
        print(f"Summarization error: {e}")
        return "Could not summarize transcript due to internal error."

def extract_keywords(transcript_text: str, top_n: int = 5):
    keywords = kw_model.extract_keywords(transcript_text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=top_n)
    return [kw[0] for kw in keywords]

def detect_emotion(transcript_text: str) -> str:
    sentiment = sia.polarity_scores(transcript_text)
    compound = sentiment['compound']
    if compound >= 0.5:
        return "Positive"
    elif compound <= -0.5:
        return "Negative"
    else:
        return "Neutral"

def generate_video_quality_score(transcript_text: str, summary: str, keywords: list) -> float:
    score = 0.0
    if len(transcript_text) > 1000:
        score += 0.4
    if len(summary.split()) > 20:
        score += 0.3
    if len(keywords) >= 3:
        score += 0.3
    return round(score, 2)

def analyze_transcript(transcript_text: str) -> dict:
    partial_text = transcript_text[:1500]  # limit to 1500 characters for speed

    summary = summarize_transcript(partial_text)
 
    keywords = extract_keywords(partial_text)

    emotion = detect_emotion(partial_text)
    
    score = generate_video_quality_score(transcript_text, summary, keywords)

    return {
        "summary": summary,
        "keywords": keywords,
        "emotion": emotion,
        "quality_score": score
    }