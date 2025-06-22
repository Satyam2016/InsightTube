import json
import re
import asyncio
from typing import List

import google.generativeai as genai

from models.schemas import TopicAnalysis
from core.config import settings
from core.logger import logger

class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    async def analyze_with_gemini(self, prompt: str) -> str:
        """Analyze content using Google Gemini"""
        try:
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            return "Analysis unavailable"

    async def generate_summary(self, transcript: str, description: str) -> str:
        """Generate video summary using Gemini"""
        content = f"Video Description: {description}\n\nTranscript: {transcript[:settings.max_transcript_length]}"
        prompt = f"""
        You are Yotube video summarizer. You will be taking the transcript text
        and summarizing the entire video and providing the important summary in points
        within 250 words. Please provide the summary of the text given here:

        {transcript}
        """
        
        return await self.analyze_with_gemini(prompt)

    async def extract_topics(self, transcript: str, description: str) -> List[TopicAnalysis]:
        """Extract topics using Gemini AI"""
        content = f"Description: {description}\n\nTranscript: {transcript[:settings.max_transcript_length]}"
        prompt = f"""
        Analyze this YouTube video content and identify the main topics discussed.
        
        {content}
        
        Return a JSON array of objects with the following structure:
        [
            {{"topic": "Topic Name", "relevance": 85, "mentions": 12}},
            ...
        ]
        
        Provide 5-8 main topics with:
        - topic: The name of the topic
        - relevance: Relevance score (0-100)
        - mentions: Estimated number of mentions
        
        Return only the JSON array, no additional text.
        """
        
        try:
            response = await self.analyze_with_gemini(prompt)
            # Try to extract JSON from response
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                topics_data = json.loads(json_match.group())
                return [TopicAnalysis(**topic) for topic in topics_data]
        except Exception as e:
            logger.error(f"Error extracting topics: {e}")
        
        # Fallback to empty list
        return []

    async def detect_emotion_with_gemini(self, text: str) -> str:
        """Detect emotion using Gemini AI"""
        try:
            prompt = f"""
            Analyze the emotion in this text and return only one word from: joy, sadness, anger, fear, surprise, disgust, neutral.
            
            Text: "{text[:500]}"
            
            Return only the emotion word, nothing else.
            """
            
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            emotion = response.text.strip().lower()
            
            # Map to standard emotions
            emotion_map = {
                'joy': 'Joy', 'happiness': 'Joy', 'happy': 'Joy',
                'sadness': 'Sadness', 'sad': 'Sadness',
                'anger': 'Anger', 'angry': 'Anger',
                'fear': 'Fear', 'afraid': 'Fear',
                'surprise': 'Surprise', 'surprised': 'Surprise',
                'disgust': 'Disgust', 'disgusted': 'Disgust',
                'neutral': 'Neutral'
            }
            
            return emotion_map.get(emotion, 'Neutral')
        except:
            return 'Neutral'

    async def extract_keywords_advanced(self, text: str, num_keywords: int = 10) -> List[str]:
        """Extract keywords using Gemini AI"""
        try:
            prompt = f"""
            Extract the {num_keywords} most important keywords from this text. 
            Return only the keywords separated by commas, no additional text.
            
            Text: "{text[:2000]}"
            """
            
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            gemini_keywords = [kw.strip() for kw in response.text.split(',')]
            
            return gemini_keywords[:num_keywords]
        except:
            return []