from contextlib import asynccontextmanager
import datetime
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
from sweepy.models.api import EventType, MarketInfo

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

    recreate_db = (
        os.getenv("RECREATE_DB", "false").lower() == "true"
        or os.getenv("ENVIRONMENT") == "development"
    )
    init_db(recreate=recreate_db)
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

try:
    app.mount("/assets", StaticFiles(directory="sweepy/static/assets"), name="assets")
except Exception as e:
    logging.warning(f"Failed to mount static files: {e}. Ensure the directory exists.")


@app.get("/")
async def serve_index():
    return FileResponse("sweepy/static/index.html")


@app.post("/api/sweepstakes")
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


@app.get("/api/sweepstakes", response_model=list[Sweepstakes])
def list_sweepstakes(
    include_closed: bool = False,
    session: Session = Depends(get_session),
) -> list[Sweepstakes]:
    """
    List all sweepstakes, optionally filtered by market_id and method.
    """
    query = select(db_models.Sweepstakes)
    if not include_closed:
        query = query.where(db_models.Sweepstakes.active)

    # TODO: Add proper pagination support
    query = query.limit(25)

    all_sweepstakes = session.exec(query).all()

    resp = [
        generate_sweepstakes.convert_db_model_to_response(sweepstake)
        for sweepstake in all_sweepstakes
    ]

    logging.info(f"Listing sweepstakes: {len(resp)} found")

    return resp


@app.get("/api/sweepstakes/{sweepstake_id}", response_model=Sweepstakes)
def get_sweepstake(
    sweepstake_id: int | str, session: Session = Depends(get_session)
) -> Sweepstakes:
    """
    Get a specific sweepstake by ID.
    """
    if isinstance(sweepstake_id, str):
        sweepstake_id = db_models.Sweepstakes.decode_stringified_id(sweepstake_id)
        if sweepstake_id is None:
            raise HTTPException(status_code=400, detail="Invalid sweepstake ID format")

    sweepstake = session.get(db_models.Sweepstakes, sweepstake_id)

    if not sweepstake:
        raise HTTPException(status_code=404, detail="Sweepstake not found")

    resp = generate_sweepstakes.convert_db_model_to_response(sweepstake)

    logging.info(f"Retrieved sweepstake: {sweepstake.id}")

    return resp


@app.post("/api/sweepstakes/{sweepstake_id}/refresh", response_model=Sweepstakes)
def refresh_sweepstake(
    sweepstake_id: int | str, session: Session = Depends(get_session)
) -> Sweepstakes:
    """
    Refresh a specific sweepstake by ID.
    """

    if isinstance(sweepstake_id, str):
        sweepstake_id = db_models.Sweepstakes.decode_stringified_id(sweepstake_id)
        if sweepstake_id is None:
            raise HTTPException(status_code=400, detail="Invalid sweepstake ID format")

    sweepstake = session.get(db_models.Sweepstakes, sweepstake_id)

    if not sweepstake:
        raise HTTPException(status_code=404, detail="Sweepstake not found")

    if not sweepstake.active:
        raise HTTPException(
            status_code=400, detail="Sweepstake is not active and cannot be refreshed"
        )

    logging.info(f"Refreshing sweepstake: {sweepstake.stringified_id}")

    updated_sweepstake = generate_sweepstakes.refresh_sweepstake(
        __bf_client, sweepstake
    )

    session.add(updated_sweepstake)
    session.commit()
    session.refresh(updated_sweepstake)

    resp = generate_sweepstakes.convert_db_model_to_response(updated_sweepstake)

    logging.info(f"Sweepstake refreshed: {updated_sweepstake.stringified_id}")

    return resp


@app.post("/api/sweepstakes/{sweepstake_id}/close", response_model=Sweepstakes)
def close_sweepstake(
    sweepstake_id: int | str, session: Session = Depends(get_session)
) -> Sweepstakes:
    """
    Close a specific sweepstake by ID.
    """

    if isinstance(sweepstake_id, str):
        sweepstake_id = db_models.Sweepstakes.decode_stringified_id(sweepstake_id)
        if sweepstake_id is None:
            raise HTTPException(status_code=400, detail="Invalid sweepstake ID format")

    sweepstake = session.get(db_models.Sweepstakes, sweepstake_id)

    if not sweepstake:
        raise HTTPException(status_code=404, detail="Sweepstake not found")

    logging.info(f"Closing sweepstake: {sweepstake.stringified_id}")

    if not sweepstake.active:
        raise HTTPException(status_code=400, detail="Sweepstake is already closed")

    logging.info(f"Sweepstake data before closing: {sweepstake.model_dump_json()}")

    sweepstake.active = False
    sweepstake.updated_at = datetime.datetime.now(datetime.timezone.utc)
    session.add(sweepstake)
    session.commit()
    session.refresh(sweepstake)

    logging.info(f"Sweepstake data after closing: {sweepstake.model_dump_json()}")

    resp = generate_sweepstakes.convert_db_model_to_response(sweepstake)

    logging.info(f"Sweepstake closed: {sweepstake.stringified_id}")

    return resp


@app.get("/api/event-types", response_model=list[EventType])
def get_event_types():
    """
    Get a list of all event types available in Betfair.
    """
    event_types = __bf_client.get_event_types()
    return [EventType(**event_type) for event_type in event_types]


@app.get("/api/markets/{event_type_id}", response_model=list[MarketInfo])
def get_outright_markets(event_type_id: str):
    """
    Get outright markets for a specific event type.
    """
    markets = __bf_client.get_outright_markets(event_type_id)

    logging.info(f"Found {len(markets)} markets for event type {event_type_id}")

    deduplicated_markets = set([MarketInfo(**market) for market in markets])

    logging.info(f"Deduplicated markets count: {len(deduplicated_markets)}")
    return list(deduplicated_markets)
