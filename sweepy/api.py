import logging
import os
import dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from sweepy.integrations.betfair import BetfairClient
from sweepy.models import SweepstakesRequest, SweepstakesResponse
from sweepy import generate_sweepstakes

app = FastAPI()

dotenv.load_dotenv()


app = FastAPI()

origins = os.getenv("FRONTEND_ORIGINS", "").split(",")

if origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    logging.warning("No origins specified in FRONTEND_ORIGINS. CORS is disabled.")


app.mount("/assets", StaticFiles(directory="sweepy/static/assets"), name="assets")


@app.get("/")
async def serve_index():
    return FileResponse("sweepy/static/index.html")


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
