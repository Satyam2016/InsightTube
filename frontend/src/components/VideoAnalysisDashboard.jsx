import React, { useState } from 'react';
import { VideoUrlInput } from './VideoUrlInput';
import { AnalysisResults } from './AnalysisResults';
import { LoadingSpinner } from './LoadingSpinner';
import { ErrorMessage } from './ErrorMessage';
import { useVideoAnalysis } from '@/hooks/useVideoAnalysis';
import { Film, Youtube } from 'lucide-react';

export const VideoAnalysisDashboard = () => {
  const [videoUrl, setVideoUrl] = useState('');
  const {
    analyzeVideo,
    analysisData,
    isLoading,
    error,
    clearAnalysis
  } = useVideoAnalysis();

  const handleAnalyze = async () => {
    if (!videoUrl) return;
    if (!videoUrl.includes('youtube.com') && !videoUrl.includes('youtu.be')) {
      return;
    }
    await analyzeVideo(videoUrl);
  };

  const handleClear = () => {
    setVideoUrl('');
    clearAnalysis();
  };

  return (
    <div className="min-h-screen p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Film className="w-12 h-12 text-red-600" />
            <h1 className="text-5xl font-bold bg-gradient-to-r from-red-600 to-red-800 bg-clip-text text-transparent">
              InsightTube
            </h1>
          </div>
          <p className="text-xl text-gray-600">
            Advanced YouTube Video Analysis Platform
          </p>
        </div>

        {/* Video URL Input */}
        <VideoUrlInput
          videoUrl={videoUrl}
          setVideoUrl={setVideoUrl}
          onAnalyze={handleAnalyze}
          onClear={handleClear}
          isLoading={isLoading}
        />

        {/* Error Display */}
        {error && <ErrorMessage message={error} />}

        {/* Loading Spinner */}
        {isLoading && <LoadingSpinner />}

        {/* Analysis Results */}
        {analysisData && !isLoading && (
          <AnalysisResults data={analysisData} />
        )}

        {/* Instructions when no analysis */}
        {!analysisData && !isLoading && !error && (
          <div className="mt-12 bg-white rounded-xl shadow-lg p-8">
            <div className="text-center mb-8">
              <Youtube className="w-16 h-16 text-red-600 mx-auto mb-4" />
              <h3 className="text-2xl font-bold text-gray-800 mb-4">
                Get Started with Video Analysis
              </h3>
              <p className="text-gray-600 mb-6">
                Enter a YouTube video URL above and click 'Analyze Video' to get comprehensive insights
              </p>
            </div>

            <div className="grid md:grid-cols-2 gap-8">
              <div>
                <h4 className="text-lg font-semibold text-gray-800 mb-4">🚀 How It Works:</h4>
                <ul className="space-y-2 text-gray-600">
                  <li>1. <strong>Enter URL:</strong> Paste any YouTube video URL</li>
                  <li>2. <strong>Click Analyze:</strong> Our AI processes the content and comments</li>
                  <li>3. <strong>Explore Results:</strong> Navigate through analysis tabs</li>
                  <li>4. <strong>Export Data:</strong> Download insights for further analysis</li>
                </ul>
              </div>

              <div>
                <h4 className="text-lg font-semibold text-gray-800 mb-4">📊 What You''ll Get:</h4>
                <ul className="space-y-2 text-gray-600">
                  <li>• <strong>Sentiment Analysis:</strong> Understand audience reactions</li>
                  <li>• <strong>Topic Extraction:</strong> Identify key themes</li>
                  <li>• <strong>Comment Analysis:</strong> Deep dive into feedback</li>
                  <li>• <strong>Performance Metrics:</strong> Comprehensive statistics</li>
                </ul>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
