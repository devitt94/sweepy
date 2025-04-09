import os
import dotenv
from fastapi import FastAPI, HTTPException

from sweepy.integrations.betfair import BetfairClient
from sweepy.models import SweepstakesRequest, SweepstakesResponse
from sweepy import generate_sweepstakes

app = FastAPI()

dotenv.load_dotenv()


betfair_client = BetfairClient(
    username=os.getenv("BETFAIR_USERNAME"),
    password=os.getenv("BETFAIR_PASSWORD"),
    app_key=os.getenv("BETFAIR_APP_KEY"),
)


@app.post("/sweepstakes")
def create_sweepstakes(request: SweepstakesRequest) -> SweepstakesResponse:
    """
    Create a new sweepstake.
    """
    # Create a new sweepstake
    try:
        response = generate_sweepstakes.generate_sweepstakes(betfair_client, request)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error creating sweepstake: {str(e)}"
        )

    return response
