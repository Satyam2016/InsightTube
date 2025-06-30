import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Badge } from '@/components/ui/badge';

export const KeywordsTab = ({ keywords }) => {
  if (!keywords || keywords.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">No keyword data available for this video.</p>
      </div>
    );
  }

  // Create frequency data (simulated based on position in array)
  const keywordsData = keywords.slice(0, 10).map((keyword, index) => ({
    keyword,
    frequency: keywords.length - index
  }));

  return (
    <div className="space-y-6 mt-6">
      <div className="grid md:grid-cols-2 gap-6">
        {/* Keywords Frequency Chart */}
        <div className="bg-gray-50 rounded-lg p-6">
          <h3 className="text-lg font-semibold mb-4">🔍 Top Keywords Frequency</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={keywordsData} layout="horizontal">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis dataKey="keyword" type="category" width={100} />
              <Tooltip />
              <Bar dataKey="frequency" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Keywords Cloud */}
        <div className="bg-gray-50 rounded-lg p-6">
          <h3 className="text-lg font-semibold mb-4">🏷️ Keywords Cloud</h3>
          <div className="flex flex-wrap gap-2 justify-center items-center h-64 overflow-y-auto">
            {keywords.slice(0, 20).map((keyword, index) => (
              <Badge 
                key={index} 
                variant="outline"
                className="text-sm py-1 px-3 bg-blue-50 hover:bg-blue-100 transition-colors"
                style={{ 
                  fontSize: `${Math.max(0.8, 1.2 - (index * 0.02))}rem`,
                }}
              >
                {keyword}
              </Badge>
            ))}
          </div>
        </div>
      </div>

      {/* Keywords Details Table */}
      <div className="bg-gray-50 rounded-lg p-6">
        <h3 className="text-lg font-semibold mb-4">📋 Keywords Details</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b">
                <th className="text-left py-2 px-4">Rank</th>
                <th className="text-left py-2 px-4">Keyword</th>
                <th className="text-left py-2 px-4">Estimated Frequency</th>
              </tr>
            </thead>
            <tbody>
              {keywordsData.map((item, index) => (
                <tr key={index} className="border-b hover:bg-white/50">
                  <td className="py-2 px-4 font-medium">#{index + 1}</td>
                  <td className="py-2 px-4">{item.keyword}</td>
                  <td className="py-2 px-4">{item.frequency}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
