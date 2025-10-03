"""
Simple test to verify the travel plan generation with just country and days
"""

import requests
import json


# Test the simplified API endpoint
def test_simple_travel_plan_generation():
    """Test the simplified travel plan generation with just country and days"""

    base_url = "http://localhost:8000/api/v1/travel-plans"

    # Test data with only country and days
    simple_input = {"country": "Japan", "days": 5}

    print("=== Testing Simple Travel Plan Generation ===")
    print(f"Input: {json.dumps(simple_input, indent=2)}")
    print()

    try:
        # Test the generation endpoint
        response = requests.post(f"{base_url}/generate", json=simple_input)

        if response.status_code == 200:
            result = response.json()
            print("✅ Generation successful!")
            print(f"Success: {result['success']}")

            if result["success"] and result["travel_plan"]:
                plan = result["travel_plan"]
                print(f"📍 Destination: {plan['country']}")
                print(f"📅 Duration: {plan['days']} days")
                print(f"🎯 Title: {plan['title']}")
                print(f"💰 Estimated Cost: ${plan['total_estimated_cost']}")
                print(
                    f"⏱️  Generation Time: {result.get('generation_time_seconds', 'N/A')} seconds"
                )
                print(f"📝 Description: {plan['description']}")
                print()
                print("📋 Sample Day (Day 1):")
                if plan["itinerary"] and len(plan["itinerary"]) > 0:
                    day1 = plan["itinerary"][0]
                    print(f"   Title: {day1['title']}")
                    print(f"   Estimated Cost: ${day1['estimated_cost']}")
                    if day1["activities"]:
                        print("   Activities:")
                        for i, activity in enumerate(
                            day1["activities"][:3]
                        ):  # Show first 3
                            print(
                                f"     {i+1}. {activity['time']}: {activity['activity']} (${activity['cost']})"
                            )
            else:
                print(
                    f"❌ Generation failed: {result.get('error_message', 'Unknown error')}"
                )

        else:
            print(f"❌ HTTP Error {response.status_code}: {response.text}")

    except requests.exceptions.ConnectionError:
        print(
            "❌ Cannot connect to the server. Make sure the FastAPI server is running on http://localhost:8000"
        )
    except Exception as e:
        print(f"❌ Error: {e}")


def test_invalid_input():
    """Test invalid input handling"""

    base_url = "http://localhost:8000/api/v1/travel-plans"

    print("\n=== Testing Invalid Input Handling ===")

    # Test invalid input (too many days)
    invalid_input = {"country": "Italy", "days": 35}

    try:
        response = requests.post(f"{base_url}/generate", json=invalid_input)
        if response.status_code == 400:
            print(f"✅ Invalid input (too many days) correctly rejected")
        else:
            result = response.json()
            if not result.get("success"):
                print(
                    f"✅ Invalid input handled gracefully: {result.get('error_message')}"
                )
            else:
                print(
                    f"❌ Invalid input test failed: expected rejection but got success"
                )
    except Exception as e:
        print(f"❌ Error testing invalid input: {e}")


if __name__ == "__main__":
    print("🚀 Testing LSEG Immersion Day Travel Plan API")
    print("=" * 50)

    # Run tests
    test_simple_travel_plan_generation()
    test_invalid_input()

    print("\n" + "=" * 50)
    print("✨ API Endpoints Available:")
    print(
        "   POST /api/v1/travel-plans/generate  - Generate travel plan with Gemini AI"
    )
    print("\n📋 Example curl command:")
    print('   curl -X POST "http://localhost:8000/api/v1/travel-plans/generate" \\')
    print('        -H "Content-Type: application/json" \\')
    print('        -d \'{"country": "Japan", "days": 5}\'')
