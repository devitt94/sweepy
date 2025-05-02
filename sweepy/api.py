from contextlib import asynccontextmanager
import logging
import os
import dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select

from sweepy.database import get_session, init_db
from sweepy import db_models
from sweepy.integrations.betfair import BetfairClient
from sweepy.models import SweepstakesRequest, Sweepstakes
from sweepy import generate_sweepstakes

dotenv.load_dotenv()
logging.basicConfig(level=logging.INFO)

__bf_client = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global __bf_client

    logging.info("Starting up the FastAPI application.")

    __bf_client = BetfairClient(
        username=os.getenv("BETFAIR_USERNAME"),
        password=os.getenv("BETFAIR_PASSWORD"),
        app_key=os.getenv("BETFAIR_APP_KEY"),
    )

    logging.info("Betfair client initialized.")

    init_db()
    logging.info("Database initialized.")

    yield

    logging.info("Shutting down the FastAPI application.")
    __bf_client = None
    logging.info("Betfair client shut down.")


app = FastAPI(lifespan=lifespan)


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


@app.post("/sweepstakes")
def create_sweepstakes(
    request: SweepstakesRequest,
    session: Session = Depends(get_session),
) -> Sweepstakes:
    """
    Create a new sweepstake.
    """

    logging.info(f"Creating sweepstake with request: {request}")

    sweepstakes_db = generate_sweepstakes.generate_sweepstakes(__bf_client, request)

    session.add(sweepstakes_db)
    session.commit()
    session.refresh(sweepstakes_db)

    response = generate_sweepstakes.convert_db_model_to_response(sweepstakes_db)

    logging.info(f"Sweepstake created: {sweepstakes_db.id}")

    return response


@app.get("/sweepstakes", response_model=list[Sweepstakes])
def list_sweepstakes(session: Session = Depends(get_session)) -> list[Sweepstakes]:
    all_sweepstakes = session.exec(select(db_models.Sweepstakes)).all()

    resp = [
        generate_sweepstakes.convert_db_model_to_response(sweepstake)
        for sweepstake in all_sweepstakes
    ]

    logging.info(f"Listing all sweepstakes: {len(resp)} found")
    return resp


@app.get("/sweepstakes/{sweepstake_id}", response_model=Sweepstakes)
def get_sweepstake(
    sweepstake_id: int, session: Session = Depends(get_session)
) -> Sweepstakes:
    """
    Get a specific sweepstake by ID.
    """
    sweepstake = session.get(db_models.Sweepstakes, sweepstake_id)

    if not sweepstake:
        raise HTTPException(status_code=404, detail="Sweepstake not found")

    resp = generate_sweepstakes.convert_db_model_to_response(sweepstake)

    logging.info(f"Retrieved sweepstake: {sweepstake.id}")

    return resp
