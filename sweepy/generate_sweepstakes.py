import datetime
from decimal import Decimal
import logging
import random

import sqlmodel
from sweepy.calculator import compute_market_probabilities
from sweepy.integrations.betfair import BetfairClient
from sweepy.integrations.live_golf.client import LiveGolfClient
from sweepy.matchmaker import get_live_golf_tournament
from sweepy.models import (
    AssignmentMethod,
    RunnerOdds,
    Runner,
    MarketNotFoundException,
    NotEnoughSelectionsException,
    SweepstakesRequest,
    Sweepstakes,
)
from sweepy import assignment
from sweepy import db_models


def get_selections(
    betfair_client: BetfairClient, market_id: str, ignore_longshots: bool
) -> list[RunnerOdds]:
    runner_names = betfair_client.get_selection_names(market_id)

    market = betfair_client.get_market_book(market_id)

    runners = []
    for runner_book in market["runners"]:
        if runner_book["status"] != "ACTIVE":
            continue
        selection_id = runner_book["selectionId"]
        runner_name = runner_names[selection_id]
        runner = Runner(
            runner_id=str(selection_id),
            name=runner_name,
            available_to_back=runner_book["ex"]["availableToBack"],
            available_to_lay=runner_book["ex"]["availableToLay"],
            last_price_traded=runner_book.get("lastPriceTraded"),
        )

        if ignore_longshots and not runner.available_to_lay:
            continue

        runners.append(runner)

    return compute_market_probabilities(runners)


def generate_sweepstakes(
    bf_client: BetfairClient,
    lg_client: LiveGolfClient,
    request: SweepstakesRequest,
    db_session: sqlmodel.Session,
) -> db_models.Sweepstakes:
    timestamp = datetime.datetime.now(datetime.timezone.utc)
    selections = get_selections(bf_client, request.market_id, request.ignore_longshots)

    bf_info = bf_client.get_market_info(request.market_id)

    if bf_info.is_golf:
        try:
            lg_tournament = get_live_golf_tournament(bf_info, lg_client)
        except ValueError as e:
            logging.error(f"Error getting Live Golf tournament: {e}")
            tournament_id = None
        else:
            tournament_id = lg_tournament.id
    else:
        tournament_id = None

    num_selections = len(selections)
    num_participants = len(request.participant_names)

    if num_selections < num_participants:
        raise NotEnoughSelectionsException(num_selections, num_participants)

    selection_assigner_func: callable[
        [list[str], list[RunnerOdds]], dict[str, list[RunnerOdds]]
    ]

    if request.method == AssignmentMethod.STAGGERED:
        selection_assigner_func = assignment.assign_selections_staggered
    elif request.method == AssignmentMethod.TIERED:
        selection_assigner_func = assignment.assign_selections_tiered
    elif request.method == AssignmentMethod.RANDOM:
        selection_assigner_func = assignment.assign_selections_random
    elif request.method == AssignmentMethod.FAIR:
        selection_assigner_func = assignment.assign_selections_fair
    else:
        raise NotImplementedError(f"Assignment method {request.method} not implemented")

    random.shuffle(request.participant_names)
    sweepstake_assignments: dict[str, list[RunnerOdds]] = selection_assigner_func(
        participants=request.participant_names,
        selections=selections,
    )

    sweepstakes_db = db_models.Sweepstakes(
        name=request.name,
        market_id=request.market_id,
        method=request.method,
        participants=[],
        active=True,
        updated_at=timestamp,
        competition=request.competition,
        tournament_id=tournament_id,
        start_date=bf_info.market_start_time,
    )

    for participant_name, selections in sweepstake_assignments.items():
        participant_equity = Decimal(0)
        participant_db = db_models.Participant(
            name=participant_name,
            sweepstake=sweepstakes_db,
            runners=[],
        )

        sorted_selections = sorted(
            selections, key=lambda x: x.implied_probability, reverse=True
        )

        runners = []
        for selection in sorted_selections:
            runner = db_models.Runner(
                name=selection.name,
                market_provider_id=selection.provider_id,
                participant=participant_db,
            )
            db_session.add(runner)

            db_session.add(
                db_models.RunnerOdds(
                    implied_probability=selection.implied_probability,
                    runner=runner,
                    timestamp=timestamp,
                )
            )

            runners.append(runner)

        participant_db.runners = runners
        for selection in sorted_selections:
            participant_equity += selection.implied_probability

        db_session.add(
            db_models.ParticipantOdds(
                implied_probability=participant_equity,
                participant=participant_db,
                timestamp=timestamp,
            )
        )
        sweepstakes_db.participants.append(participant_db)

    db_session.add(sweepstakes_db)
    db_session.commit()

    return sweepstakes_db


def convert_db_model_to_response(
    sweepstakes_db: db_models.Sweepstakes,
) -> Sweepstakes:
    """
    Convert the database model to the API model.
    """

    jsondata = sweepstakes_db.model_dump()
    jsondata["id"] = sweepstakes_db.stringified_id
    participants = [
        {
            "name": participant.name,
            "equity": participant.latest_odds.implied_probability,
            "assignments": [
                {
                    "provider_id": runner.market_provider_id,
                    "name": runner.name,
                    "implied_probability": runner.latest_odds.implied_probability,
                    "score": runner.score,
                }
                for runner in participant.runners
            ],
        }
        for participant in sweepstakes_db.participants
    ]

    jsondata["participants"] = participants
    jsondata["updated_at"] = sweepstakes_db.updated_at.isoformat()
    return Sweepstakes(**jsondata)


def refresh_sweepstake_odds(
    client: BetfairClient,
    sweepstake_db: db_models.Sweepstakes,
    session: sqlmodel.Session,
) -> db_models.Sweepstakes:
    """
    Refresh the sweepstake by re-fetching the market data and updating the participants.
    """

    latest_data = get_selections(client, sweepstake_db.market_id, False)
    fetched_at = datetime.datetime.now(datetime.timezone.utc)
    if not latest_data:
        raise MarketNotFoundException(
            f"Market not found for market_id {sweepstake_db.market_id}."
        )

    for participant in sweepstake_db.participants:
        logging.info(f"Refreshing participant: {participant.name}")
        # Update each participant's runners with the latest data
        seen = set()
        updated_equity = Decimal(0)
        for runner in participant.runners:
            # Find the latest runner data
            if runner.market_provider_id in seen:
                continue

            seen.add(runner.market_provider_id)
            latest_runner = next(
                (r for r in latest_data if r.provider_id == runner.market_provider_id),
                None,
            )
            if latest_runner:
                p = latest_runner.implied_probability
            else:
                # If the runner is not found in the latest data, keep the old one but assume probability is 0
                logging.warning(
                    f"Runner {runner.name} with market_provider_id {runner.market_provider_id} not found in latest data."
                )
                p = 0.0

            updated_runner_odds = db_models.RunnerOdds(
                implied_probability=p,
                runner=runner,
                timestamp=fetched_at,
            )
            session.add(updated_runner_odds)
            session.add(runner)
            updated_equity += Decimal(p)

        # Recalculate equity based on updated odds
        updated_participant_odds = db_models.ParticipantOdds(
            implied_probability=updated_equity,
            participant=participant,
            timestamp=fetched_at,
        )

        session.add(updated_participant_odds)
        session.add(participant)

    sweepstake_db.updated_at = fetched_at
    session.add(sweepstake_db)
    session.commit()
    logging.info(f"Refreshed sweepstake odds: {sweepstake_db.id}")
    return sweepstake_db


def refresh_sweepstake_leaderboard(
    client: LiveGolfClient,
    sweepstake_db: db_models.Sweepstakes,
    session: sqlmodel.Session,
):
    """
    Refresh the sweepstakes leaderboard by re-fetching the market data and updating the participants.
    """

    if not sweepstake_db.tournament_id:
        raise ValueError(
            f"Sweepstake {sweepstake_db.id} does not have a tournament ID."
        )

    leaderboard_data = client.get_leaderboard(
        sweepstake_db.start_date.year, sweepstake_db.tournament_id
    )

    score_map = {
        player["playerId"]: player["total"]
        for player in leaderboard_data["leaderboardRows"]
    }

    for participant in sweepstake_db.participants:
        for runner in participant.runners:
            if runner.score_provider_id is None:
                continue

            # Update the score for the runner
            if runner.score_provider_id in score_map:
                score = score_map[runner.score_provider_id]
                if score == "-":
                    score = None
                elif score == "E":
                    score = 0
                else:
                    score = int(score)
            else:
                logging.warning(
                    f"Runner {runner.name} with score_provider_id {runner.score_provider_id} not found in leaderboard data."
                )
                score = None

            session.add(runner)

    session.commit()
    logging.info(f"Refreshed sweepstakes leaderboard for {sweepstake_db.id}")
