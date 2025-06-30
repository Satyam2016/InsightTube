import React from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent } from '@/components/ui/card';
import { Link, Trash2, Play } from 'lucide-react';

export const VideoUrlInput = ({
  videoUrl,
  setVideoUrl,
  onAnalyze,
  onClear,
  isLoading
}) => {
  const isValidUrl = videoUrl.includes('youtube.com') || videoUrl.includes('youtu.be');

  return (
    <Card className="mb-8 bg-white/80 backdrop-blur-sm shadow-lg">
      <CardContent className="p-6">
        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
          <Link className="w-5 h-5 text-red-600" />
          Enter YouTube Video URL
        </h2>
        
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <Input
              type="url"
              value={videoUrl}
              onChange={(e) => setVideoUrl(e.target.value)}
              placeholder="https://www.youtube.com/watch?v=..."
              className="text-base"
              disabled={isLoading}
            />
            {videoUrl && !isValidUrl && (
              <p className="text-red-500 text-sm mt-1">
                Please enter a valid YouTube URL
              </p>
            )}
          </div>
          
          <div className="flex gap-2">
            <Button
              onClick={onAnalyze}
              disabled={!videoUrl || !isValidUrl || isLoading}
              className="bg-red-600 hover:bg-red-700 text-white px-6"
            >
              {isLoading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2" />
                  Analyzing...
                </>
              ) : (
                <>
                  <Play className="w-4 h-4 mr-2" />
                  Analyze Video
                </>
              )}
            </Button>
            
            <Button
              onClick={onClear}
              variant="outline"
              disabled={isLoading}
              className="px-4"
            >
              <Trash2 className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};
