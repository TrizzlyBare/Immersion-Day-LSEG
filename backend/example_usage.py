#!/usr/bin/env python3
"""
Example script demonstrating travel plan generation with country and days input
that integrates with Gemini AI for the LSEG Immersion Day project.
"""

import asyncio
import json
from app.services.gemini_service import GeminiService
from app.schemas.travelplan import TravelPlanInput, TravelPreference, BudgetRange
from datetime import date, timedelta


async def main():
    """Demonstrate travel plan generation"""

    print("=== LSEG Immersion Day - Travel Plan Generation Demo ===\n")

    # Example 1: Japan trip
    print("Example 1: Generating a 7-day Japan itinerary...")
    japan_input = TravelPlanInput(
        country="Japan",
        days=7,
        start_date=date.today() + timedelta(days=30),
        budget_range=BudgetRange.MODERATE,
        preferences=[
            TravelPreference.CULTURE,
            TravelPreference.FOOD,
            TravelPreference.HISTORY,
        ],
        group_size=2,
        additional_requirements="Interested in cherry blossom season and traditional ryokans",
    )

    gemini_service = GeminiService()
    japan_plan = await gemini_service.generate_travel_plan(
        country=japan_input.country,
        days=japan_input.days,
        preferences=japan_input.preferences,
        budget_range=japan_input.budget_range,
        group_size=japan_input.group_size,
        additional_requirements=japan_input.additional_requirements,
        start_date=japan_input.start_date,
    )

    if japan_plan:
        print(f"✅ Generated plan: {japan_plan.title}")
        print(f"📍 Destination: {japan_plan.country}")
        print(f"📅 Duration: {japan_plan.days} days")
        print(f"💰 Estimated cost: ${japan_plan.total_estimated_cost}")
        print(f"📝 Description: {japan_plan.description}")
        print(f"🎯 Itinerary highlights:")
        for day in japan_plan.itinerary[:3]:  # Show first 3 days
            print(f"   - {day.title} (${day.estimated_cost})")
        print()

    # Example 2: Thailand adventure
    print("Example 2: Generating a 5-day Thailand adventure...")
    thailand_input = TravelPlanInput(
        country="Thailand",
        days=5,
        budget_range=BudgetRange.BUDGET,
        preferences=[
            TravelPreference.ADVENTURE,
            TravelPreference.NATURE,
            TravelPreference.FOOD,
        ],
        group_size=1,
        additional_requirements="Looking for outdoor activities and authentic street food",
    )

    thailand_plan = await gemini_service.generate_travel_plan(
        country=thailand_input.country,
        days=thailand_input.days,
        preferences=thailand_input.preferences,
        budget_range=thailand_input.budget_range,
        group_size=thailand_input.group_size,
        additional_requirements=thailand_input.additional_requirements,
    )

    if thailand_plan:
        print(f"✅ Generated plan: {thailand_plan.title}")
        print(f"📍 Destination: {thailand_plan.country}")
        print(f"📅 Duration: {thailand_plan.days} days")
        print(f"💰 Estimated cost: ${thailand_plan.total_estimated_cost}")
        print(f"🎯 Daily activities sample:")
        for activity in thailand_plan.itinerary[0].activities[
            :2
        ]:  # Show first 2 activities of day 1
            print(
                f"   - {activity['time']}: {activity['activity']} (${activity['cost']})"
            )
        print()

    # Example 3: Luxury European getaway
    print("Example 3: Generating a 10-day luxury European tour...")
    europe_input = TravelPlanInput(
        country="Italy",
        days=10,
        budget_range=BudgetRange.LUXURY,
        preferences=[
            TravelPreference.CULTURE,
            TravelPreference.HISTORY,
            TravelPreference.FOOD,
        ],
        group_size=4,
        additional_requirements="Focus on Renaissance art, fine dining, and luxury accommodations",
    )

    europe_plan = await gemini_service.generate_travel_plan(
        country=europe_input.country,
        days=europe_input.days,
        preferences=europe_input.preferences,
        budget_range=europe_input.budget_range,
        group_size=europe_input.group_size,
        additional_requirements=europe_input.additional_requirements,
    )

    if europe_plan:
        print(f"✅ Generated plan: {europe_plan.title}")
        print(f"📍 Destination: {europe_plan.country}")
        print(f"📅 Duration: {europe_plan.days} days")
        print(f"💰 Estimated cost: ${europe_plan.total_estimated_cost}")
        print(f"👥 Group size: {europe_input.group_size} people")
        print()

    print("=== Key Features of the Backend ===")
    print("✅ Accepts country and travel days as primary input")
    print("✅ Integrates with Gemini AI for intelligent itinerary generation")
    print("✅ Supports various preferences (culture, food, adventure, etc.)")
    print("✅ Handles different budget ranges (budget, moderate, luxury)")
    print("✅ Provides structured daily itineraries with activities and costs")
    print("✅ Validates input parameters before processing")
    print("✅ Returns detailed travel plans with estimates and recommendations")

    print("\n=== API Endpoints Available ===")
    print("POST /api/v1/travel-plans/generate - Generate with Gemini AI")
    print("POST /api/v1/travel-plans/validate-input - Validate travel input")
    print("GET  /api/v1/travel-plans/ - Get all travel plans")
    print("GET  /api/v1/travel-plans/{id} - Get specific travel plan")
    print("PUT  /api/v1/travel-plans/{id} - Update travel plan")
    print("DELETE /api/v1/travel-plans/{id} - Delete travel plan")


if __name__ == "__main__":
    asyncio.run(main())
