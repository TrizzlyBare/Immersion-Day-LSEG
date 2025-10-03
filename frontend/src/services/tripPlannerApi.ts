import type { TripFormData, TripPlan } from "../components/TripPlannerForm";

export async function generateTripPlan(formData: TripFormData): Promise<TripPlan> {
  await new Promise((resolve) => setTimeout(resolve, 600));

  const days = Math.max(1, Math.min(30, Number(formData.days || 1)));

  const itinerary: TripPlan["itinerary"] = Array.from({ length: days }).map((_, idx) => {
    const dayNumber = idx + 1;
    return {
      day: dayNumber,
      title: `Explore ${formData.country} - Day ${dayNumber}`,
      activities: [
        `Morning walk in a popular district of ${formData.country}`,
        `Lunch at a recommended local spot`,
        `Visit a landmark or museum`,
      ],
      recommendations: [
        `Try a regional specialty dish`,
        `Use public transit or walk for short distances`,
      ],
    };
  });

  const baseBudgetPerDay = 120;
  const low = baseBudgetPerDay * days;
  const high = Math.round(low * 1.6);

  const plan: TripPlan = {
    destination: formData.country,
    duration: days,
    itinerary,
    estimatedBudget: {
      low,
      high,
      currency: "USD",
    },
    bestTimeToVisit: "Spring and Autumn for mild weather and fewer crowds",
    essentialTips: [
      "Carry a small daypack with water and sunscreen",
      "Learn a few basic local phrases for courtesy",
      "Have offline maps downloaded in advance",
    ],
  };

  return plan;
}


