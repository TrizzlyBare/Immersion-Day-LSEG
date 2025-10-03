from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from datetime import date as DateType


class TravelPlanInput(BaseModel):
    """Simple input schema - only country and days required"""

    country: str = Field(..., description="Destination country for travel")
    days: int = Field(..., ge=1, le=30, description="Number of travel days (1-30)")


class DayItinerary(BaseModel):
    """Single day itinerary details"""

    day_number: int = Field(..., description="Day number in the trip")
    day_date: Optional[DateType] = Field(None, description="Date of this day")
    title: str = Field(..., description="Title/theme for the day")
    activities: List[Dict[str, Any]] = Field(
        default=[], description="List of activities for the day"
    )
    estimated_cost: Optional[float] = Field(
        None, description="Estimated cost for the day"
    )
    notes: Optional[str] = Field(None, description="Additional notes for the day")


class TravelPlan(BaseModel):
    """Complete travel plan schema - no database storage needed"""

    country: str = Field(..., description="Destination country")
    days: int = Field(..., description="Total number of days")
    title: str = Field(..., description="Travel plan title")
    description: Optional[str] = Field(None, description="Travel plan description")
    itinerary: List[DayItinerary] = Field(default=[], description="Daily itinerary")
    gemini_generated: bool = Field(
        default=True, description="Whether plan was AI-generated"
    )


class GeminiGenerationResponse(BaseModel):
    """Response schema from Gemini AI generation"""

    success: bool
    travel_plan: Optional[TravelPlan] = None
    error_message: Optional[str] = None
    generation_time_seconds: Optional[float] = None
