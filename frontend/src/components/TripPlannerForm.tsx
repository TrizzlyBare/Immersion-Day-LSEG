import React, { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';

export interface TripFormData {
  country: string;
  days: number;
}

export interface TripPlan {
  destination: string;
  duration: number;
  itinerary: Array<{
    day: number;
    title: string;
    activities: string[];
    recommendations: string[];
  }>;
  estimatedBudget: {
    low: number;
    high: number;
    currency: string;
  };
  bestTimeToVisit: string;
  essentialTips: string[];
}

interface TripPlannerFormProps {
  onGenerate: (formData: TripFormData) => Promise<TripPlan>;
}

export default function TripPlannerForm({ onGenerate }: TripPlannerFormProps) {
  const [formData, setFormData] = useState<TripFormData>({
    country: '',
    days: 1
  });
  const [isLoading, setIsLoading] = useState(false);
  const [tripPlan, setTripPlan] = useState<TripPlan | null>(null);
  const [error, setError] = useState<string>('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.country.trim()) {
      setError('Please enter a country');
      return;
    }
    
    if (formData.days < 1 || formData.days > 30) {
      setError('Please enter a valid number of days (1-30)');
      return;
    }

    setIsLoading(true);
    setError('');
    
    try {
      const plan = await onGenerate(formData);
      setTripPlan(plan);
    } catch (err) {
      setError('Failed to generate trip plan. Please try again.');
      console.error('Trip generation error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCountryChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({ ...prev, country: e.target.value }));
  };

  const handleDaysChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const days = parseInt(e.target.value) || 1;
    setFormData(prev => ({ ...prev, days }));
  };

  return (
    <div className="w-full max-w-4xl mx-auto space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Plan Your Trip</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="country">Country</Label>
                <Input
                  id="country"
                  type="text"
                  placeholder="e.g., Japan, Italy, Thailand"
                  value={formData.country}
                  onChange={handleCountryChange}
                  required
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="days">Number of Days</Label>
                <Input
                  id="days"
                  type="number"
                  min="1"
                  max="30"
                  placeholder="e.g., 7"
                  value={formData.days}
                  onChange={handleDaysChange}
                  required
                />
              </div>
            </div>
            
            {error && (
              <div className="text-destructive text-sm">{error}</div>
            )}
            
            <Button 
              type="submit" 
              className="w-full" 
              disabled={isLoading}
            >
              {isLoading ? 'Generating Trip Plan...' : 'Generate Trip Plan'}
            </Button>
          </form>
        </CardContent>
      </Card>

      {tripPlan && (
        <Card>
          <CardHeader>
            <CardTitle>Your Trip to {tripPlan.destination}</CardTitle>
            <p className="text-muted-foreground">{tripPlan.duration} days</p>
          </CardHeader>
          <CardContent className="space-y-6">
            <div>
              <h3>Estimated Budget</h3>
              <p>{tripPlan.estimatedBudget.currency} {tripPlan.estimatedBudget.low} - {tripPlan.estimatedBudget.high}</p>
            </div>
            
            <div>
              <h3>Best Time to Visit</h3>
              <p>{tripPlan.bestTimeToVisit}</p>
            </div>
            
            <div>
              <h3>Daily Itinerary</h3>
              <div className="space-y-4">
                {tripPlan.itinerary.map((day) => (
                  <Card key={day.day}>
                    <CardHeader>
                      <CardTitle>Day {day.day}: {day.title}</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-3">
                        <div>
                          <h4>Activities</h4>
                          <ul className="list-disc list-inside space-y-1">
                            {day.activities.map((activity, index) => (
                              <li key={index}>{activity}</li>
                            ))}
                          </ul>
                        </div>
                        
                        <div>
                          <h4>Recommendations</h4>
                          <ul className="list-disc list-inside space-y-1">
                            {day.recommendations.map((rec, index) => (
                              <li key={index}>{rec}</li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
            
            <div>
              <h3>Essential Tips</h3>
              <ul className="list-disc list-inside space-y-1">
                {tripPlan.essentialTips.map((tip, index) => (
                  <li key={index}>{tip}</li>
                ))}
              </ul>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}