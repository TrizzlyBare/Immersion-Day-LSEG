import json
import asyncio
from typing import List
import google.generativeai as genai
from app.schemas.travelplan import TravelPlan, DayItinerary
from app.core.config import settings


class GeminiService:
    """Service for handling Gemini AI travel plan generation"""

    def __init__(self):
        # Initialize the Gemini AI client
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)

    async def generate_travel_plan(self, country: str, days: int) -> TravelPlan:
        """
        Generate a travel plan using Gemini AI
        """
        try:
            # Create the prompt for Gemini
            prompt = self._create_travel_prompt(country, days)

            # Generate content using Gemini AI
            response = await self._call_gemini_api(prompt)

            # Parse the response and create TravelPlan object
            return self._parse_gemini_response(response, country, days)

        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            # Fallback to mock response if API fails
            return self._generate_mock_plan(country, days)

    def _create_travel_prompt(self, country: str, days: int) -> str:
        """Create a structured prompt for Gemini AI"""
        return f"""
        Create a detailed {days}-day travel itinerary for {country}. 
        
        Please provide the response in the following JSON format:
        {{
            "country": "{country}",
            "days": {days},
            "itinerary": [
                {{
                    "day": 1,
                    "title": "Day title",
                    "activities": [
                        "Activity 1",
                        "Activity 2",
                        "Activity 3"
                    ],
                    "notes": "Additional notes for the day"
                }}
            ],
            "budget_estimate": "Estimated budget range",
            "best_time_to_visit": "Best time to visit information",
            "cultural_tips": "Cultural tips and etiquette"
        }}
        
        Include popular attractions, local experiences, restaurants, and practical tips.
        Make sure each day has 3-5 activities and provide helpful notes.
        """

    async def _call_gemini_api(self, prompt: str) -> str:
        """Call Gemini API asynchronously"""
        try:
            # Generate content
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Gemini API call failed: {e}")

    def _parse_gemini_response(
        self, response_text: str, country: str, days: int
    ) -> TravelPlan:
        """Parse Gemini's response into TravelPlan object"""
        try:
            # Try to extract JSON from the response
            # Sometimes Gemini wraps JSON in code blocks
            response_text = response_text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            response_data = json.loads(response_text)

            # Create DayItinerary objects
            itinerary = []
            for day_data in response_data.get("itinerary", []):
                day_itinerary = DayItinerary(
                    day=day_data.get("day", 1),
                    title=day_data.get("title", f"Day {day_data.get('day', 1)}"),
                    activities=day_data.get("activities", []),
                    notes=day_data.get("notes", ""),
                )
                itinerary.append(day_itinerary)

            # Create and return TravelPlan
            return TravelPlan(
                country=response_data.get("country", country),
                days=response_data.get("days", days),
                itinerary=itinerary,
                budget_estimate=response_data.get(
                    "budget_estimate", "Budget information not available"
                ),
                best_time_to_visit=response_data.get(
                    "best_time_to_visit", "Year-round"
                ),
                cultural_tips=response_data.get(
                    "cultural_tips", "No specific cultural tips provided"
                ),
            )

        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error parsing Gemini response: {e}")
            # If parsing fails, try to create a basic plan from the text
            return self._create_fallback_plan(response_text, country, days)

    def _create_fallback_plan(
        self, response_text: str, country: str, days: int
    ) -> TravelPlan:
        """Create a fallback plan when JSON parsing fails"""
        # Create basic itinerary from response text
        itinerary = []
        for day in range(1, days + 1):
            day_itinerary = DayItinerary(
                day=day,
                title=f"Day {day}: Explore {country}",
                activities=[
                    f"Morning: Visit local attractions",
                    f"Afternoon: Experience local culture",
                    f"Evening: Try traditional cuisine",
                ],
                notes=f"Activities for day {day} in {country}",
            )
            itinerary.append(day_itinerary)

        return TravelPlan(
            country=country,
            days=days,
            itinerary=itinerary,
            budget_estimate="Budget varies depending on preferences",
            best_time_to_visit="Year-round",
            cultural_tips="Respect local customs and traditions",
        )

    def _generate_mock_plan(self, country: str, days: int) -> TravelPlan:
        """Generate a mock travel plan for fallback purposes"""
        itinerary = []

        for day in range(1, days + 1):
            activities = [
                f"Visit top attractions in {country}",
                f"Experience local culture and traditions",
                f"Try authentic {country} cuisine",
                f"Explore historical sites",
                f"Shop for local souvenirs",
            ]

            # Select 3-4 activities for each day
            selected_activities = activities[: min(4, len(activities))]

            day_itinerary = DayItinerary(
                day=day,
                title=f"Day {day}: Discover {country}",
                activities=selected_activities,
                notes=f"Make sure to bring comfortable walking shoes and a camera for day {day}.",
            )
            itinerary.append(day_itinerary)

        return TravelPlan(
            country=country,
            days=days,
            itinerary=itinerary,
            budget_estimate=f"Estimated budget: $100-200 per day for {country}",
            best_time_to_visit=f"Best time to visit {country} varies by season",
            cultural_tips=f"Learn basic phrases in the local language and respect cultural norms in {country}",
        )
