# Complete API Documentation - LSEG Immersion Day Travel Plan API

## 🚀 Server Information

- **Base URL**: `http://localhost:8000`
- **Framework**: FastAPI
- **API Version**: v1
- **Documentation**: Available at `/docs` (Swagger UI) and `/redoc` (ReDoc)

## 📋 All Available APIs

### 1. Root & Health Check APIs

#### **GET /**

**Root endpoint - Welcome message**

```bash
curl -X GET "http://localhost:8000/"
```

**Response:**

```json
{
  "message": "Welcome to LSEG Immersion Day API",
  "status": "healthy",
  "docs": "/docs"
}
```

---

#### **GET /health**

**Health check endpoint**

```bash
curl -X GET "http://localhost:8000/health"
```

**Response:**

```json
{
  "status": "healthy"
}
```

---

### 2. Travel Plan Generation API

#### **POST /api/v1/v1/generate**

**Generate AI-powered travel plan with Gemini AI**

**Request:**

```bash
curl -X POST "http://localhost:8000/api/v1/v1/generate" \
     -H "Content-Type: application/json" \
     -d '{
       "country": "Japan",
       "days": 5
     }'
```

**Request Body Schema:**

```json
{
  "country": "string (required)",
  "days": "integer (1-30, required)"
}
```

**Response Schema:**

```json
{
  "success": "boolean",
  "travel_plan": {
    "country": "string",
    "days": "integer",
    "title": "string",
    "description": "string",
    "total_estimated_cost": "float",
    "currency": "string",
    "itinerary": [
      {
        "day_number": "integer",
        "day_date": "date",
        "title": "string",
        "activities": [
          {
            "time": "string",
            "activity": "string",
            "location": "string",
            "cost": "float",
            "duration": "string"
          }
        ],
        "estimated_cost": "float",
        "notes": "string"
      }
    ],
    "gemini_generated": "boolean"
  },
  "error_message": "string",
  "generation_time_seconds": "float"
}
```

**Success Response Example:**

```json
{
  "success": true,
  "travel_plan": {
    "country": "Japan",
    "days": 5,
    "title": "Amazing 5-Day Japan Adventure",
    "description": "Experience the best of Japan in 5 days with this AI-curated itinerary featuring diverse experiences.",
    "total_estimated_cost": 500.0,
    "currency": "USD",
    "itinerary": [
      {
        "day_number": 1,
        "day_date": "2025-11-02",
        "title": "Day 1: Arrival & Japan Introduction",
        "activities": [
          {
            "time": "09:00",
            "activity": "Breakfast at local cafe",
            "location": "City center",
            "cost": 15,
            "duration": "1 hour"
          },
          {
            "time": "10:30",
            "activity": "Visit main attraction",
            "location": "Tourist district",
            "cost": 25,
            "duration": "2-3 hours"
          },
          {
            "time": "14:00",
            "activity": "Lunch at traditional restaurant",
            "location": "Local neighborhood",
            "cost": 20,
            "duration": "1.5 hours"
          },
          {
            "time": "16:00",
            "activity": "Explore local market",
            "location": "Market district",
            "cost": 10,
            "duration": "2 hours"
          },
          {
            "time": "19:00",
            "activity": "Dinner at recommended restaurant",
            "location": "Entertainment district",
            "cost": 35,
            "duration": "2 hours"
          }
        ],
        "estimated_cost": 100.0,
        "notes": "Weather is typically good in Japan during this time. Bring comfortable walking shoes."
      }
    ],
    "gemini_generated": true
  },
  "error_message": null,
  "generation_time_seconds": 1.2
}
```

**Error Response Example:**

```json
{
  "success": false,
  "travel_plan": null,
  "error_message": "Travel plans longer than 30 days are not supported",
  "generation_time_seconds": null
}
```

**HTTP Status Codes:**

- `200`: Success - Travel plan generated successfully
- `400`: Bad Request - Invalid input (days > 14, empty country, etc.)
- `500`: Internal Server Error - AI generation failed

---

### 3. Interactive API Documentation

#### **GET /docs**

**Swagger UI - Interactive API documentation**

Access at: `http://localhost:8000/docs`

Features:

- Interactive API testing
- Request/response schemas
- Try-it-out functionality
- Authentication testing

---

#### **GET /redoc**

**ReDoc - Alternative API documentation**

Access at: `http://localhost:8000/redoc`

Features:

- Clean, readable documentation
- Detailed schema information
- Code examples
- Download OpenAPI spec

---

#### **GET /api/v1/openapi.json**

**OpenAPI JSON specification**

```bash
curl -X GET "http://localhost:8000/api/v1/openapi.json"
```

Returns the complete OpenAPI 3.0 specification in JSON format.

---

## 🔧 API Features & Configuration

### Input Validation

- **Country**: Must be non-empty string
- **Days**: Must be integer between 1-14 (currently limited to 14 days max)
- **Content-Type**: Must be `application/json`

### CORS Configuration

The API supports Cross-Origin Resource Sharing (CORS) with the following origins:

- `http://localhost:3000`
- `http://localhost:8080`
- `http://localhost:8000`

### AI Integration

- **AI Provider**: Google Gemini AI
- **Generation Time**: Typically 1-3 seconds
- **Fallback**: Mock generation if AI service unavailable

### Response Format

All APIs return JSON responses with consistent structure:

- Success responses include requested data
- Error responses include error details
- HTTP status codes indicate operation result

---

## 🧪 Testing the APIs

### Using cURL

```bash
# Health check
curl -X GET "http://localhost:8000/health"

# Generate travel plan
curl -X POST "http://localhost:8000/api/v1/v1/generate" \
     -H "Content-Type: application/json" \
     -d '{"country": "Thailand", "days": 7}'
```

### Using Python requests

```python
import requests

# Health check
response = requests.get("http://localhost:8000/health")
print(response.json())

# Generate travel plan
payload = {"country": "Italy", "days": 10}
response = requests.post(
    "http://localhost:8000/api/v1/v1/generate",
    json=payload
)
print(response.json())
```

### Using JavaScript fetch

```javascript
// Health check
fetch("http://localhost:8000/health")
  .then((response) => response.json())
  .then((data) => console.log(data));

// Generate travel plan
fetch("http://localhost:8000/api/v1/v1/generate", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    country: "France",
    days: 6,
  }),
})
  .then((response) => response.json())
  .then((data) => console.log(data));
```

---

## 📊 API Summary

| Endpoint               | Method | Purpose              | Input          | Output               |
| ---------------------- | ------ | -------------------- | -------------- | -------------------- |
| `/`                    | GET    | Welcome message      | None           | Status message       |
| `/health`              | GET    | Health check         | None           | Health status        |
| `/api/v1/v1/generate`  | POST   | Generate travel plan | Country + Days | Complete travel plan |
| `/docs`                | GET    | Interactive docs     | None           | Swagger UI           |
| `/redoc`               | GET    | API documentation    | None           | ReDoc interface      |
| `/api/v1/openapi.json` | GET    | OpenAPI spec         | None           | JSON specification   |

---

## 🎯 Key Points

1. **Simplicity**: Only 2 inputs required (country, days)
2. **AI-Powered**: Uses Gemini AI for intelligent travel planning
3. **No Database**: Stateless - generate and return immediately
4. **Rich Output**: Detailed daily itineraries with activities, costs, timing
5. **Error Handling**: Comprehensive validation and error responses
6. **Documentation**: Auto-generated interactive documentation
7. **CORS Enabled**: Ready for frontend integration
8. **Fast**: Typical response time 1-3 seconds

This API is designed specifically for the LSEG Immersion Day demo, focusing on simplicity and powerful AI-generated travel planning capabilities.
