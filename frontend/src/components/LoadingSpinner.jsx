import React, { useState, useEffect } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';

export const LoadingSpinner = () => {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setProgress((oldProgress) => {
        const newProgress = oldProgress + 2;
        return newProgress > 90 ? 90 : newProgress;
      });
    }, 100);

    return () => clearInterval(timer);
  }, []);

  return (
    <Card className="mb-8 bg-white/80 backdrop-blur-sm shadow-lg">
      <CardContent className="p-8 text-center">
        <div className="flex flex-col items-center space-y-4">
          <div className="animate-spin rounded-full h-12 w-12 border-4 border-red-600 border-t-transparent"></div>
          <h3 className="text-xl font-semibold text-gray-800">
            Analyzing Video...
          </h3>
          <p className="text-gray-600 max-w-md">
            This may take a few minutes while we process the video content, comments, and perform sentiment analysis.
          </p>
          <div className="w-full max-w-md">
            <Progress value={progress} className="h-2" />
            <p className="text-sm text-gray-500 mt-2">
              Processing... {progress}%
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};
