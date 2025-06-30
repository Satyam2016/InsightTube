import React from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { VideoMetrics } from './VideoMetrics';
import { OverviewTab } from './OverviewTab';
import { TopicsTab } from './TopicsTab';
import { SentimentTab } from './SentimentTab';
import { CommentsTab } from './CommentsTab';
import { KeywordsTab } from './KeywordsTab';
import { ExportSection } from './ExportSection';

export const AnalysisResults = ({ data }) => {
  return (
    <div className="space-y-8">
      {/* Video Title and Basic Info */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h2 className="text-2xl font-bold text-blue-600 mb-2">
          📺 {data.video_data.title}
        </h2>
        <p className="text-gray-600 mb-4">
          <strong>Channel:</strong> {data.video_data.channel} | 
          <strong> Duration:</strong> {data.video_data.duration} | 
          <strong> Upload Date:</strong> {data.video_data.upload_date}
        </p>
      </div>

      {/* Key Metrics */}
      <VideoMetrics data={data.video_data} />

      {/* Analysis Tabs */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <Tabs defaultValue="overview" className="w-full">
          <TabsList className="grid w-full grid-cols-5 lg:grid-cols-5">
            <TabsTrigger value="overview">📊 Overview</TabsTrigger>
            <TabsTrigger value="topics">🎯 Topics</TabsTrigger>
            <TabsTrigger value="sentiment">😊 Sentiment</TabsTrigger>
            <TabsTrigger value="comments">💬 Comments</TabsTrigger>
            <TabsTrigger value="keywords">🔍 Keywords</TabsTrigger>
          </TabsList>

          <TabsContent value="overview">
            <OverviewTab data={data} />
          </TabsContent>

          <TabsContent value="topics">
            <TopicsTab topics={data.topics_data} />
          </TabsContent>

          <TabsContent value="sentiment">
            <SentimentTab 
              sentimentData={data.sentiment_data}
              timelineData={data.sentiment_timeline}
            />
          </TabsContent>

          <TabsContent value="comments">
            <CommentsTab 
              comments={data.top_comments}
              totalComments={data.video_data.comments}
            />
          </TabsContent>

          <TabsContent value="keywords">
            <KeywordsTab keywords={data.keywords} />
          </TabsContent>
        </Tabs>
      </div>

      {/* Export Section */}
      <ExportSection data={data} />
    </div>
  );
};
