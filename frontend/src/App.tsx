import TripPlannerForm from './components/TripPlannerForm';
import { generateTripPlan } from './services/tripPlannerApi';

export default function App() {
  return (
    <div className="min-h-screen bg-background p-6">
      <div className="container mx-auto">
        <div className="text-center mb-8">
          <h1 className="mb-2">Trip Planner</h1>
          <p className="text-muted-foreground">Plan your perfect getaway with personalized itineraries</p>
        </div>
        
        <TripPlannerForm onGenerate={generateTripPlan} />
      </div>
    </div>
  );
}