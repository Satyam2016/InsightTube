import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Eye, ThumbsUp, MessageCircle, TrendingUp, Clock } from 'lucide-react';

export const VideoMetrics = ({ data }) => {
  const calculateEngagementRate = () => {
    const viewsStr = data.views.replace(/[^\d.]/g, '');
    let viewsNum = parseFloat(viewsStr);
    
    if (data.views.includes('K')) viewsNum *= 1000;
    if (data.views.includes('M')) viewsNum *= 1000000;
    
    if (viewsNum > 0) {
      const engagement = ((data.likes + data.comments) / viewsNum) * 100;
      return engagement.toFixed(2);
    }
    return 'N/A';
  };

  const metrics = [
    {
      icon: Eye,
      label: 'Views',
      value: data.views,
      color: 'text-blue-600'
    },
    {
      icon: ThumbsUp,
      label: 'Likes',
      value: data.likes.toLocaleString(),
      color: 'text-green-600'
    },
    {
      icon: MessageCircle,
      label: 'Comments',
      value: data.comments.toLocaleString(),
      color: 'text-purple-600'
    },
    {
      icon: TrendingUp,
      label: 'Engagement',
      value: `${calculateEngagementRate()}%`,
      color: 'text-orange-600'
    },
    {
      icon: Clock,
      label: 'Processing Time',
      value: `${data.processing_time.toFixed(1)}s`,
      color: 'text-gray-600'
    }
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
      {metrics.map((metric, index) => (
        <Card key={index} className="bg-gradient-to-br from-white to-gray-50 hover:shadow-lg transition-shadow">
          <CardContent className="p-4 text-center">
            <metric.icon className={`w-8 h-8 mx-auto mb-2 ${metric.color}`} />
            <div className="font-bold text-lg text-gray-800">
              {metric.value}
            </div>
            <div className="text-sm text-gray-600">
              {metric.label}
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
};
