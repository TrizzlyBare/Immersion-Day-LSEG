from fastapi import APIRouter, HTTPException
from app.schemas.travelplan import (
    TravelPlanInput,
    GeminiGenerationResponse,
)
from app.services.gemini_service import GeminiService

router = APIRouter()


@router.post("/generate_plan", response_model=GeminiGenerationResponse)
async def generate_travel_plan(travel_input: TravelPlanInput):
    """Generate a travel plan using Gemini AI with just country and days"""
    try:
        # Validate input
        if travel_input.days > 14:
            raise HTTPException(
                status_code=400,
                detail="Travel plans longer than 30 days are not supported",
            )

        if not travel_input.country.strip():
            raise HTTPException(status_code=400, detail="Country is required")

        # Initialize Gemini service
        gemini_service = GeminiService()

        # Generate travel plan using Gemini AI
        generated_plan = await gemini_service.generate_travel_plan(
            country=travel_input.country,
            days=travel_input.days,
        )

        if generated_plan:
            return GeminiGenerationResponse(
                success=True,
                travel_plan=generated_plan,
                generation_time_seconds=gemini_service.last_generation_time,
            )
        else:
            return GeminiGenerationResponse(
                success=False, error_message="Failed to generate travel plan"
            )

    except HTTPException:
        raise
    except Exception as e:
        return GeminiGenerationResponse(
            success=False, error_message=f"Error generating travel plan: {str(e)}"
        )
