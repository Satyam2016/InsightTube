import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ThumbsUp, User } from 'lucide-react';

export const CommentsTab = ({ comments, totalComments }) => {
  const getSentimentColor = (sentiment) => {
    switch (sentiment) {
      case 'positive': return 'bg-green-100 text-green-800 border-green-200';
      case 'negative': return 'bg-red-100 text-red-800 border-red-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getSentimentBorderColor = (sentiment) => {
    switch (sentiment) {
      case 'positive': return 'border-l-green-500';
      case 'negative': return 'border-l-red-500';
      default: return 'border-l-gray-500';
    }
  };

  if (!comments || comments.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">No comment data available for this video.</p>
      </div>
    );
  }

  const avgSentimentScore = comments.reduce((sum, comment) => sum + comment.sentiment_score, 0) / comments.length;
  const totalLikes = comments.reduce((sum, comment) => sum + comment.likes, 0);

  return (
    <div className="space-y-6 mt-6">
      {/* Comment Statistics */}
      <div className="grid md:grid-cols-3 gap-4 mb-6">
        <Card className="bg-gradient-to-br from-blue-50 to-blue-100">
          <CardContent className="p-4 text-center">
            <div className="text-2xl font-bold text-blue-800">
              {totalComments.toLocaleString()}
            </div>
            <div className="text-sm text-blue-600">Total Comments</div>
          </CardContent>
        </Card>
        
        <Card className="bg-gradient-to-br from-purple-50 to-purple-100">
          <CardContent className="p-4 text-center">
            <div className="text-2xl font-bold text-purple-800">
              {avgSentimentScore.toFixed(3)}
            </div>
            <div className="text-sm text-purple-600">Avg Sentiment Score</div>
          </CardContent>
        </Card>
        
        <Card className="bg-gradient-to-br from-orange-50 to-orange-100">
          <CardContent className="p-4 text-center">
            <div className="text-2xl font-bold text-orange-800">
              {totalLikes.toLocaleString()}
            </div>
            <div className="text-sm text-orange-600">Top Comments Likes</div>
          </CardContent>
        </Card>
      </div>

      {/* Top Comments */}
      <div>
        <h3 className="text-lg font-semibold mb-4">💬 Top Comments Analysis</h3>
        <div className="space-y-4">
          {comments.map((comment, index) => (
            <Card key={index} className={`border-l-4 ${getSentimentBorderColor(comment.sentiment)}`}>
              <CardContent className="p-4">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <User className="w-5 h-5 text-gray-600" />
                    <span className="font-medium text-gray-800">{comment.author}</span>
                    <div className="flex items-center gap-2 text-sm text-gray-600">
                      <ThumbsUp className="w-4 h-4" />
                      {comment.likes}
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Badge className={getSentimentColor(comment.sentiment)}>
                      {comment.sentiment}
                    </Badge>
                    <span className="text-xs text-gray-500">
                      ({comment.sentiment_score.toFixed(3)})
                    </span>
                  </div>
                </div>
                <p className="text-gray-700 leading-relaxed">"{comment.text}"</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};
