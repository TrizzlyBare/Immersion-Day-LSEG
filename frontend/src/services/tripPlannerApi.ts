import type { TripFormData, TripPlan } from "../components/TripPlannerForm";

export async function generateTripPlan(formData: TripFormData): Promise<TripPlan> {
  const response = await fetch("/api/v1/generate_plan", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ country: formData.country, days: formData.days }),
  });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  const data = await response.json();

  if (!data?.success) {
    throw new Error(data?.error_message || "Backend returned an error");
  }

  const backendPlan = data.travel_plan || {};

  const destination: string = backendPlan.country || formData.country;
  const duration: number = backendPlan.days || Number(formData.days) || 1;

  const itinerary: TripPlan["itinerary"] = (backendPlan.itinerary || []).map((d: any, idx: number) => {
    const dayNumber = d.day ?? d.day_number ?? idx + 1;
    const title = d.title || `Day ${dayNumber}`;
    // Normalize activities to string[]
    const rawActivities = d.activities || [];
    const activities = rawActivities.map((a: any) => {
      if (typeof a === "string") return a;
      if (a?.activity) return String(a.activity);
      try { return JSON.stringify(a); } catch { return String(a); }
    });
    // Recommendations not provided by backend; derive from notes if present
    const recommendations: string[] = d.recommendations || (d.notes ? [String(d.notes)] : []);
    return { day: dayNumber, title, activities, recommendations };
  });

  // Derive budget since backend may return a string field
  const baseBudgetPerDay = 120;
  const low = baseBudgetPerDay * duration;
  const high = Math.round(low * 1.6);

  const plan: TripPlan = {
    destination,
    duration,
    itinerary,
    estimatedBudget: { low, high, currency: "USD" },
    bestTimeToVisit: backendPlan.best_time_to_visit || "Year-round",
    essentialTips: backendPlan.cultural_tips
      ? String(backendPlan.cultural_tips).split(/\.\s+/).filter(Boolean)
      : ["Respect local customs and plan ahead"],
  };

  return plan;
}


