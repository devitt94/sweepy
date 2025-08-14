import asyncio
import logging
import os
import dotenv
from sqlalchemy import select
from sweepy import db_models, generate_sweepstakes, database
from sweepy.integrations import betfair

REDIS_URL = os.getenv("REDIS_URL")

dotenv.load_dotenv()
REFRESH_INTERVAL = int(os.getenv("REFRESH_INTERVAL", 900))


async def refresh_all_sweepstakes_task(
    bf_client: betfair.BetfairClient, delay_seconds: int = REFRESH_INTERVAL
):
    """
    Task to refresh all sweepstakes.
    """
    while True:
        logging.info("Starting to refresh all sweepstakes.")
        with database.get_session_context() as db_session:
            statement = select(db_models.Sweepstakes).where(
                db_models.Sweepstakes.active
            )

            all_active_sweepstakes = db_session.exec(statement).scalars().all()
            if not all_active_sweepstakes:
                logging.info("No active sweepstakes found.")
            else:
                for sweepstake in all_active_sweepstakes:
                    logging.info(f"Refreshing sweepstake: {sweepstake.id}")
                    generate_sweepstakes.refresh_sweepstake(
                        client=bf_client,
                        sweepstake_db=sweepstake,
                        session=db_session,
                    )

            logging.info("All active sweepstakes have been refreshed.")

        logging.info(f"Waiting for {delay_seconds} seconds before the next refresh.")
        await asyncio.sleep(delay_seconds)
