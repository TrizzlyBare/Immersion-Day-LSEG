import json
import time
import asyncio
from typing import Optional, List
from datetime import datetime, timedelta
from app.schemas.travelplan import (
    TravelPlan,
    DayItinerary,
    TravelPreference,
    BudgetRange,
)
from datetime import date as DateType


class GeminiService:
    """Service for handling Gemini AI travel plan generation"""

    def __init__(self):
        self.last_generation_time = 0.0
        # In production, you would initialize the actual Gemini AI client here
        # self.gemini_client = genai.GenerativeModel('gemini-pro')

    async def generate_travel_plan(
        self,
        country: str,
        days: int,
        preferences: Optional[List[TravelPreference]] = None,
        budget_range: Optional[BudgetRange] = None,
        group_size: int = 1,
        additional_requirements: Optional[str] = None,
        start_date: Optional[DateType] = None,
    ) -> Optional[TravelPlan]:
        """Generate a travel plan using Gemini AI"""

        start_time = time.time()

        try:
            # Set defaults for None values
            if budget_range is None:
                budget_range = BudgetRange.MODERATE
            if preferences is None:
                preferences = []

            # Create the prompt for Gemini AI
            prompt = self._create_gemini_prompt(
                country,
                days,
                preferences,
                budget_range,
                group_size,
                additional_requirements,
                start_date,
            )

            # Simulate AI generation delay (replace with actual Gemini AI call)
            await asyncio.sleep(1.0)  # Simulate processing time

            # For demo purposes, generate a mock response
            # In production, replace this with actual Gemini AI API call
            generated_plan = self._generate_mock_plan(
                country, days, preferences, budget_range, start_date
            )

            self.last_generation_time = time.time() - start_time
            return generated_plan

        except Exception as e:
            print(f"Error generating travel plan: {e}")
            return None

    def _create_gemini_prompt(
        self,
        country: str,
        days: int,
        preferences: Optional[List[TravelPreference]],
        budget_range: BudgetRange,
        group_size: int,
        additional_requirements: Optional[str],
        start_date: Optional[DateType],
    ) -> str:
        """Create a structured prompt for Gemini AI"""

        preferences_str = (
            ", ".join([pref.value for pref in preferences])
            if preferences
            else "general tourism"
        )

        prompt = f"""
        Create a detailed {days}-day travel itinerary for {country}.
        
        Requirements:
        - Destination: {country}
        - Duration: {days} days
        - Group size: {group_size} people
        - Budget preference: {budget_range.value}
        - Interests: {preferences_str}
        """

        if start_date:
            prompt += f"\n- Start date: {start_date.strftime('%Y-%m-%d')}"

        if additional_requirements:
            prompt += f"\n- Additional requirements: {additional_requirements}"

        prompt += """
        
        Please provide:
        1. A catchy title for the trip
        2. Brief description of the travel plan
        3. Day-by-day itinerary with:
           - Main activities and attractions
           - Estimated costs per day
           - Practical tips and notes
        4. Total estimated budget
        
        Format the response as a structured travel plan with clear daily breakdowns.
        """

        return prompt

    def _generate_mock_plan(
        self,
        country: str,
        days: int,
        preferences: Optional[List[TravelPreference]],
        budget_range: BudgetRange,
        start_date: Optional[DateType],
    ) -> TravelPlan:
        """Generate a mock travel plan for demo purposes"""

        # Budget multipliers based on preference
        budget_multipliers = {
            BudgetRange.BUDGET: 50,
            BudgetRange.MODERATE: 100,
            BudgetRange.LUXURY: 200,
        }

        daily_budget = budget_multipliers[budget_range]

        # Generate daily itinerary
        itinerary = []
        current_date = start_date

        for day in range(1, days + 1):
            if current_date:
                day_date = current_date + timedelta(days=day - 1)
            else:
                day_date = None

            # Mock activities based on preferences
            activities = self._generate_mock_activities(preferences, budget_range, day)

            day_itinerary = DayItinerary(
                day_number=day,
                day_date=day_date,
                title=f"Day {day}: {self._get_day_theme(day, country, preferences)}",
                activities=activities,
                estimated_cost=daily_budget
                * (0.8 + (day % 3) * 0.1),  # Vary daily costs
                notes=f"Weather is typically good in {country} during this time. Bring comfortable walking shoes.",
            )
            itinerary.append(day_itinerary)

        # Create the travel plan
        plan = TravelPlan(
            country=country,
            days=days,
            title=f"Amazing {days}-Day {country} Adventure",
            description=f"Experience the best of {country} in {days} days with this AI-curated itinerary featuring {', '.join([p.value for p in preferences]) if preferences else 'diverse experiences'}.",
            total_estimated_cost=daily_budget * days,
            currency="USD",
            itinerary=itinerary,
            gemini_generated=True,
        )

        return plan

    def _get_day_theme(
        self, day: int, country: str, preferences: Optional[List[TravelPreference]]
    ) -> str:
        """Generate a theme for each day"""
        themes = [
            f"Arrival & {country} Introduction",
            f"Cultural Exploration",
            f"Local Cuisine & Markets",
            f"Historical Sites",
            f"Nature & Outdoor Activities",
            f"Art & Museums",
            f"Local Neighborhoods",
            f"Adventure Activities",
            f"Relaxation & Wellness",
            f"Shopping & Souvenirs",
            f"Departure & Final Experiences",
        ]

        if preferences and day <= len(preferences):
            pref = preferences[day - 1]
            if pref == TravelPreference.CULTURE:
                return "Cultural Immersion"
            elif pref == TravelPreference.FOOD:
                return "Culinary Journey"
            elif pref == TravelPreference.ADVENTURE:
                return "Adventure & Thrills"
            elif pref == TravelPreference.NATURE:
                return "Nature Exploration"
            elif pref == TravelPreference.HISTORY:
                return "Historical Discovery"

        return themes[min(day - 1, len(themes) - 1)]

    def _generate_mock_activities(
        self,
        preferences: Optional[List[TravelPreference]],
        budget_range: BudgetRange,
        day: int,
    ) -> List[dict]:
        """Generate mock activities for a day"""

        base_activities = [
            {
                "time": "09:00",
                "activity": "Breakfast at local cafe",
                "location": "City center",
                "cost": 15,
                "duration": "1 hour",
            },
            {
                "time": "10:30",
                "activity": "Visit main attraction",
                "location": "Tourist district",
                "cost": 25,
                "duration": "2-3 hours",
            },
            {
                "time": "14:00",
                "activity": "Lunch at traditional restaurant",
                "location": "Local neighborhood",
                "cost": 20,
                "duration": "1.5 hours",
            },
            {
                "time": "16:00",
                "activity": "Explore local market",
                "location": "Market district",
                "cost": 10,
                "duration": "2 hours",
            },
            {
                "time": "19:00",
                "activity": "Dinner at recommended restaurant",
                "location": "Entertainment district",
                "cost": 35,
                "duration": "2 hours",
            },
        ]

        # Adjust costs based on budget preference
        cost_multiplier = 1.0
        if budget_range == BudgetRange.BUDGET:
            cost_multiplier = 0.6
        elif budget_range == BudgetRange.LUXURY:
            cost_multiplier = 2.0

        for activity in base_activities:
            activity["cost"] = int(activity["cost"] * cost_multiplier)

        return base_activities
