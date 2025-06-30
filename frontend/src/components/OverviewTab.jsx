import React from 'react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export const OverviewTab = ({ data }) => {
  const performanceMetrics = [
    {
      name: 'Sentiment Score',
      score: data.sentiment_data.find(s => s.name === 'Positive')?.value || 0,
      maxScore: 100
    },
    {
      name: 'Topic Relevance',
      score: data.topics_data.length > 0
        ? data.topics_data.reduce((sum, topic) => sum + topic.relevance, 0) / data.topics_data.length
        : 0,
      maxScore: 100
    },
    {
      name: 'Comment Engagement',
      score: Math.min(100, (data.video_data.comments / Math.max(1, data.video_data.likes)) * 100),
      maxScore: 100
    }
  ];

  return (
    <div className="space-y-6 mt-6">
      <div className="grid md:grid-cols-2 gap-6">
        {/* Sentiment Distribution */}
        <div className="bg-gray-50 rounded-lg p-6">
          <h3 className="text-lg font-semibold mb-4">📈 Overall Sentiment Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={data.sentiment_data}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: ${value}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {data.sentiment_data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Performance Metrics */}
        <div className="bg-gray-50 rounded-lg p-6">
          <h3 className="text-lg font-semibold mb-4">📊 Video Performance Metrics</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={performanceMetrics}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" angle={-45} textAnchor="end" height={80} />
              <YAxis />
              <Tooltip />
              <Bar dataKey="score" fill="#dc2626" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};
