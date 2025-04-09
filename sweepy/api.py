import os
import dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sweepy.integrations.betfair import BetfairClient
from sweepy.models import SweepstakesRequest, SweepstakesResponse
from sweepy import generate_sweepstakes

app = FastAPI()

dotenv.load_dotenv()


app = FastAPI()


origins = [
    "http://localhost:5173",  # Vite default dev server
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

    response = generate_sweepstakes.generate_sweepstakes(betfair_client, request)

    return response
