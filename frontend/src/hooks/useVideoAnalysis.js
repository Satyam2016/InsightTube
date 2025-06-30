import { useState } from 'react';

const API_BASE_URL = "http://127.0.0.1:8000";
const API_KEY = "test_key";

export const useVideoAnalysis = () => {
  const [analysisData, setAnalysisData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const analyzeVideo = async (videoUrl) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/analyze`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${API_KEY}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          video_url: videoUrl,
          include_comments: true,
          include_sentiment: true,
          include_topics: true,
          include_keywords: true
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const apiData = await response.json();
      const processedData = processApiResponse(apiData);

      if (processedData) {
        setAnalysisData(processedData);
      } else {
        throw new Error('Failed to process analysis results');
      }
    } catch (err) {
      console.error('Analysis error:', err);
      setError(err.message || 'An unexpected error occurred');

      // For demo purposes, let's provide mock data if the API fails
      setAnalysisData(getMockData());
    } finally {
      setIsLoading(false);
    }
  };

  const clearAnalysis = () => {
    setAnalysisData(null);
    setError(null);
  };

  return { analyzeVideo, analysisData, isLoading, error, clearAnalysis };
};

const processApiResponse = (apiData) => {
  try {
    const video_info = apiData.video_info || {};

    const video_data = {
      title: video_info.title || 'Unknown Title',
      channel: video_info.channel || 'Unknown Channel',
      views: video_info.views || '0 views',
      upload_date: video_info.upload_date || 'Unknown date',
      duration: video_info.duration || '0:00',
      likes: video_info.likes || 0,
      dislikes: video_info.dislikes || 0,
      comments: video_info.comments || 0,
      processing_time: apiData.processing_time || 0
    };

    const topics_data = (apiData.topics || []).map(topic => ({
      topic: topic.topic || '',
      relevance: topic.relevance || 0,
      mentions: topic.mentions || 0
    }));

    const sentiment_data = (apiData.sentiment_distribution || []).map(sentiment => ({
      name: sentiment.name || '',
      value: sentiment.value || 0,
      color: sentiment.color || '#000000'
    }));

    const sentiment_timeline = (apiData.sentiment_over_time || []).map(segment => ({
      time: segment.time || '',
      positive: segment.positive || 0,
      negative: segment.negative || 0,
      neutral: segment.neutral || 0
    }));

    const top_comments = (apiData.top_comments || []).map(comment => ({
      author: comment.author || 'Unknown',
      text: comment.text || '',
      sentiment: comment.sentiment || 'neutral',
      sentiment_score: comment.sentiment_score || 0,
      likes: comment.likes || 0
    }));

    const keywords = apiData.comment_analysis?.top_keywords || [];

    return {
      video_data,
      topics_data,
      sentiment_data,
      sentiment_timeline,
      top_comments,
      keywords
    };
  } catch (error) {
    console.error('Error processing API response:', error);
    return null;
  }
};

const getMockData = () => ({
  video_data: {
    title: "Sample YouTube Video Analysis",
    channel: "Demo Channel",
    views: "1.2M views",
    upload_date: "2 days ago",
    duration: "15:30",
    likes: 45000,
    dislikes: 1200,
    comments: 8500,
    processing_time: 45.2
  },
  topics_data: [
    { topic: "Technology", relevance: 85, mentions: 120 },
    { topic: "Innovation", relevance: 72, mentions: 95 },
    { topic: "Future", relevance: 68, mentions: 80 },
    { topic: "AI", relevance: 65, mentions: 75 }
  ],
  sentiment_data: [
    { name: "Positive", value: 68, color: "#22c55e" },
    { name: "Neutral", value: 22, color: "#64748b" },
    { name: "Negative", value: 10, color: "#ef4444" }
  ],
  sentiment_timeline: [
    { time: "0-25%", positive: 65, negative: 15, neutral: 20 },
    { time: "25-50%", positive: 70, negative: 10, neutral: 20 },
    { time: "50-75%", positive: 68, negative: 12, neutral: 20 },
    { time: "75-100%", positive: 72, negative: 8, neutral: 20 }
  ],
  top_comments: [
    {
      author: "TechEnthusiast",
      text: "This is absolutely amazing! The future of technology looks so bright.",
      sentiment: "positive",
      sentiment_score: 0.95,
      likes: 1250
    },
    {
      author: "CuriousViewer",
      text: "Great explanation, but I wish there were more examples shown.",
      sentiment: "neutral",
      sentiment_score: 0.15,
      likes: 890
    },
    {
      author: "SkepticalUser",
      text: "I'm not convinced this will work in practice. Too many limitations.",
      sentiment: "negative",
      sentiment_score: -0.75,
      likes: 320
    }
  ],
  keywords: ["technology", "innovation", "future", "AI", "machine learning", "automation", "digital", "trends", "development", "breakthrough"]
});
