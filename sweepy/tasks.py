import asyncio
from collections.abc import Iterable
import logging
import os
import dotenv
from sqlalchemy import select, and_
from sweepy import db_models, generate_sweepstakes, database
from sweepy.integrations import betfair
from sweepy.integrations.live_golf.client import LiveGolfClient

REDIS_URL = os.getenv("REDIS_URL")

dotenv.load_dotenv()
MARKET_REFRESH_INTERVAL = int(os.getenv("MARKET_REFRESH_INTERVAL", 900))
SCORE_REFRESH_INTERVAL = int(os.getenv("SCORE_REFRESH_INTERVAL", 3000))


async def refresh_all_odds_task(
    bf_client: betfair.BetfairClient,
    delay_seconds: int = MARKET_REFRESH_INTERVAL,
):
    """
    Task to refresh odds for all active sweepstakes.
    """

    if delay_seconds <= 0:
        return

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
                    logging.info(f"Refreshing sweepstake: {sweepstake.stringified_id}")
                    generate_sweepstakes.refresh_sweepstake_odds(
                        client=bf_client,
                        sweepstake_db=sweepstake,
                        session=db_session,
                    )

            logging.info("Odds for all active sweepstakes have been refreshed.")

        logging.info(f"Waiting for {delay_seconds} seconds before the next refresh.")
        await asyncio.sleep(delay_seconds)


async def refresh_all_scores_task(
    lg_client: LiveGolfClient,
    delay_seconds: int = SCORE_REFRESH_INTERVAL,
):
    """
    Task to refresh all scores.
    """

    if delay_seconds <= 0:
        return

    while True:
        logging.info("Starting to refresh all scores.")
        with database.get_session_context() as db_session:
            statement = select(db_models.Sweepstakes).where(
                and_(
                    db_models.Sweepstakes.active,
                    db_models.Sweepstakes.tournament_id.isnot(None),
                )
            )

            all_active_sweepstakes: Iterable[db_models.Sweepstakes] = (
                db_session.exec(statement).scalars().all()
            )
            if not all_active_sweepstakes:
                logging.info("No active sweepstakes found with scores linked.")
            else:
                for sweepstake in all_active_sweepstakes:
                    logging.info(
                        f"Refreshing scores for sweepstake: {sweepstake.stringified_id}"
                    )
                    generate_sweepstakes.refresh_sweepstake_leaderboard(
                        client=lg_client,
                        sweepstake_db=sweepstake,
                        session=db_session,
                    )

            logging.info("All active scores have been refreshed.")

        logging.info(f"Waiting for {delay_seconds} seconds before the next refresh.")
        await asyncio.sleep(delay_seconds)
