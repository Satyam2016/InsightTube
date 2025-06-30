import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { AlertCircle } from 'lucide-react';

export const ErrorMessage = ({ message }) => {
  return (
    <Card className="mb-8 border-red-200 bg-red-50">
      <CardContent className="p-6">
        <div className="flex items-center gap-3">
          <AlertCircle className="w-6 h-6 text-red-600" />
          <div>
            <h3 className="font-semibold text-red-800">Analysis Error</h3>
            <p className="text-red-700">{message}</p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};
