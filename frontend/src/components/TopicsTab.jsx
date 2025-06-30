import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ScatterChart,
  Scatter
} from 'recharts';

export const TopicsTab = ({ topics }) => {
  if (!topics || topics.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">No topic data available for this video.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6 mt-6">
      <div className="grid md:grid-cols-2 gap-6">
        {/* Topic Relevance Chart */}
        <div className="bg-gray-50 rounded-lg p-6">
          <h3 className="text-lg font-semibold mb-4">🎯 Topic Relevance Scores</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={topics} layout="horizontal">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis dataKey="topic" type="category" width={100} />
              <Tooltip />
              <Bar dataKey="relevance" fill="#dc2626" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Topic Mentions vs Relevance */}
        <div className="bg-gray-50 rounded-lg p-6">
          <h3 className="text-lg font-semibold mb-4">📊 Topic Mentions vs Relevance</h3>
          <ResponsiveContainer width="100%" height={300}>
            <ScatterChart data={topics}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="mentions" name="Mentions" />
              <YAxis dataKey="relevance" name="Relevance" />
              <Tooltip cursor={{ strokeDasharray: '3 3' }} />
              <Scatter dataKey="relevance" fill="#dc2626" />
            </ScatterChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Detailed Topic Breakdown */}
      <div className="bg-gray-50 rounded-lg p-6">
        <h3 className="text-lg font-semibold mb-4">📋 Detailed Topic Breakdown</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b">
                <th className="text-left py-2 px-4">Topic</th>
                <th className="text-left py-2 px-4">Relevance (%)</th>
                <th className="text-left py-2 px-4">Mentions</th>
              </tr>
            </thead>
            <tbody>
              {topics.map((topic, index) => (
                <tr key={index} className="border-b hover:bg-white/50">
                  <td className="py-2 px-4 font-medium">{topic.topic}</td>
                  <td className="py-2 px-4">{topic.relevance.toFixed(1)}%</td>
                  <td className="py-2 px-4">{topic.mentions}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
