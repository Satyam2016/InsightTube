import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts';
import { Card, CardContent } from '@/components/ui/card';
import { Smile, Meh, Frown } from 'lucide-react';

export const SentimentTab = ({ sentimentData, timelineData }) => {
  const getSentimentIcon = (name) => {
    switch (name.toLowerCase()) {
      case 'positive':
        return <Smile className="w-8 h-8 text-green-600" />;
      case 'negative':
        return <Frown className="w-8 h-8 text-red-600" />;
      default:
        return <Meh className="w-8 h-8 text-gray-600" />;
    }
  };

  return (
    <div className="space-y-6 mt-6">
      {/* Sentiment Timeline */}
      {timelineData && timelineData.length > 0 && (
        <div className="bg-gray-50 rounded-lg p-6">
          <h3 className="text-lg font-semibold mb-4">😊 Sentiment Analysis Over Time</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={timelineData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="positive" stroke="#22c55e" strokeWidth={3} />
              <Line type="monotone" dataKey="negative" stroke="#ef4444" strokeWidth={3} />
              <Line type="monotone" dataKey="neutral" stroke="#64748b" strokeWidth={3} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Sentiment Summary Cards */}
      <div className="grid md:grid-cols-3 gap-4">
        {sentimentData.map((sentiment, index) => (
          <Card key={index} className="bg-gradient-to-br from-white to-gray-50">
            <CardContent className="p-6 text-center">
              <div className="flex justify-center mb-3">
                {getSentimentIcon(sentiment.name)}
              </div>
              <div className="text-2xl font-bold text-gray-800 mb-1">
                {sentiment.value}%
              </div>
              <div className="text-sm text-gray-600">
                {sentiment.name} Comments
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};
