import React from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Download } from 'lucide-react';

export const ExportSection = ({ data }) => {
  const exportToCsv = (dataArray, filename) => {
    if (!dataArray || dataArray.length === 0) return;
    
    const headers = Object.keys(dataArray[0]);
    const csvContent = [
      headers.join(','),
      ...dataArray.map(row =>
        headers.map(header =>
          JSON.stringify(row[header] || '')
        ).join(',')
      )
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${filename}_${new Date().toISOString().slice(0, 10)}.csv`;
    link.click();
    window.URL.revokeObjectURL(url);
  };

  const exportToJson = () => {
    const reportData = {
      video_info: data.video_data,
      topics: data.topics_data,
      sentiment_data: data.sentiment_data,
      sentiment_timeline: data.sentiment_timeline,
      top_comments: data.top_comments,
      keywords: data.keywords,
      analysis_timestamp: new Date().toISOString()
    };

    const blob = new Blob([JSON.stringify(reportData, null, 2)], { type: 'application/json' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `insighttube_analysis_${new Date().toISOString().slice(0, 10)}.json`;
    link.click();
    window.URL.revokeObjectURL(url);
  };

  return (
    <Card className="bg-gradient-to-r from-gray-50 to-gray-100">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Download className="w-5 h-5 text-gray-600" />
          💾 Export Analysis Data
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid md:grid-cols-3 gap-4">
          <Button
            onClick={() => exportToCsv(data.topics_data, 'topics_analysis')}
            variant="outline"
            className="w-full"
            disabled={!data.topics_data || data.topics_data.length === 0}
          >
            📥 Download Topics CSV
          </Button>
          
          <Button
            onClick={() => exportToCsv(data.top_comments, 'comments_analysis')}
            variant="outline"
            className="w-full"
            disabled={!data.top_comments || data.top_comments.length === 0}
          >
            📥 Download Comments CSV
          </Button>
          
          <Button
            onClick={exportToJson}
            variant="outline"
            className="w-full bg-blue-50 hover:bg-blue-100"
          >
            📥 Download Full Report
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};
