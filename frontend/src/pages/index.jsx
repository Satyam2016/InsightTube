import React, { useState } from 'react';
import { VideoAnalysisDashboard } from '@/components/VideoAnalysisDashboard';

const Index = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 to-blue-50">
      <VideoAnalysisDashboard />
    </div>
  );
};

export default Index;