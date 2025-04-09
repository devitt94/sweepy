from fastapi import APIRouter, HTTPException

from sweepy.models import SweepstakesRequest, SweepstakesResponse
from sweepy import generate_sweepstakes

app = APIRouter()


@app.post("/sweepstakes")
def create_sweepstakes(request: SweepstakesRequest) -> SweepstakesResponse:
    """
    Create a new sweepstake.
    """
    # Validate the request
    if not request.participants:
        raise HTTPException(status_code=400, detail="Participants list cannot be empty")

    # Create a new sweepstake
    try:
        response = generate_sweepstakes.generate_sweepstakes(request)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error creating sweepstake: {str(e)}"
        )

    return response
