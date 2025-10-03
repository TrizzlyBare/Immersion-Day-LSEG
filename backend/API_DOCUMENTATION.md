# Travel Plan API - Simplified Input

This API is designed for the LSEG Immersion Day project and accepts only **2 simple inputs**:

1. **Country** - The destination country for travel
2. **Days** - The number of travel days (1-30)

## Key Features

✅ **Simple Input**: Only country and days required  
✅ **Gemini AI Integration**: Generates intelligent travel itineraries  
✅ **Structured Output**: Detailed day-by-day plans with activities and costs  
✅ **Input Validation**: Ensures valid country names and day ranges  
✅ **RESTful API**: Standard HTTP endpoints for easy integration

## API Endpoint

### Generate Travel Plan

**POST** `/api/v1/travel-plans/generate`

**That's it!** Just one simple endpoint that takes country and days, returns a complete travel plan.

**Request Body:**

```json
{
  "country": "Japan",
  "days": 5
}
```

**Response:**

```json
{
  "success": true,
  "travel_plan": {
    "country": "Japan",
    "days": 5,
    "title": "Amazing 5-Day Japan Adventure",
    "description": "Experience the best of Japan in 5 days...",
    "total_estimated_cost": 500,
    "currency": "USD",
    "itinerary": [
      {
        "day_number": 1,
        "title": "Day 1: Arrival & Japan Introduction",
        "activities": [
          {
            "time": "09:00",
            "activity": "Breakfast at local cafe",
            "location": "City center",
            "cost": 15,
            "duration": "1 hour"
          }
        ],
        "estimated_cost": 100,
        "notes": "Weather is typically good in Japan during this time."
      }
    ],
    "created_at": "2025-10-03T00:00:00",
    "gemini_generated": true
  },
  "generation_time_seconds": 1.2
}
```

### 2. Validate Input

**POST** `/api/v1/travel-plans/validate-input`

**Request Body:**

```json
{
  "country": "Thailand",
  "days": 7
}
```

**Response:**

```json
{
  "valid": true,
  "message": "Travel input is valid",
  "estimated_generation_time": "~14 seconds"
}
```

### 3. List All Travel Plans

**GET** `/api/v1/travel-plans/`

**Response:**

```json
[
  {
    "id": 1,
    "country": "Japan",
    "days": 5,
    "title": "Amazing 5-Day Japan Adventure",
    "total_estimated_cost": 500
  }
]
```

### 4. Get Specific Travel Plan

**GET** `/api/v1/travel-plans/{id}`

Returns the complete travel plan with full itinerary details.

## Input Validation Rules

- **Country**: Must be a non-empty string
- **Days**: Must be between 1 and 30 (inclusive)
- Both fields are required

## Example Usage

### cURL Command

```bash
curl -X POST "http://localhost:8000/api/v1/travel-plans/generate" \
     -H "Content-Type: application/json" \
     -d '{"country": "Japan", "days": 5}'
```

### Python Example

```python
import requests

# Generate a travel plan
response = requests.post(
    "http://localhost:8000/api/v1/travel-plans/generate",
    json={"country": "Thailand", "days": 7}
)

if response.status_code == 200:
    result = response.json()
    if result['success']:
        plan = result['travel_plan']
        print(f"Generated plan: {plan['title']}")
        print(f"Total cost: ${plan['total_estimated_cost']}")
```

### JavaScript/Frontend Example

```javascript
const generateTravelPlan = async (country, days) => {
  const response = await fetch("/api/v1/travel-plans/generate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ country, days }),
  });

  const result = await response.json();
  if (result.success) {
    return result.travel_plan;
  } else {
    throw new Error(result.error_message);
  }
};

// Usage
generateTravelPlan("Italy", 10)
  .then((plan) => console.log("Travel plan:", plan))
  .catch((error) => console.error("Error:", error));
```

## Generated Travel Plan Structure

Each generated travel plan includes:

- **Basic Info**: Country, days, title, description
- **Cost Estimation**: Total estimated cost in USD
- **Daily Itinerary**: Day-by-day breakdown with:
  - Day number and title/theme
  - List of activities with times, locations, and costs
  - Estimated daily cost
  - Practical notes and tips
- **Metadata**: Creation time, AI generation status

## How It Works

1. **Input Processing**: API receives country and days
2. **Validation**: Checks input validity and constraints
3. **AI Generation**: Sends structured prompt to Gemini AI
4. **Response Processing**: Parses AI response into structured format
5. **Storage**: Saves generated plan (demo uses in-memory storage)
6. **Return**: Sends complete travel plan back to client

## Running the API

1. Start the FastAPI server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

2. Access the interactive documentation:

   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

3. Test the API:

```bash
python test_simple_api.py
```

## Integration Notes

- The API is designed to be called from a frontend application
- Responses are in JSON format for easy parsing
- Error handling includes proper HTTP status codes
- CORS is configured for frontend integration
- All dates and times are in ISO format
- Costs are provided in USD (configurable in future versions)

This simplified design makes it perfect for the LSEG Immersion Day demo where users only need to specify their destination country and trip duration to get a complete AI-generated travel itinerary.
