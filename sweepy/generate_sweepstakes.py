from decimal import Decimal
import random
from sweepy.calculator import compute_market_probabilities
from sweepy.integrations.betfair import BetfairClient
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
    try:
        runner_names = betfair_client.get_selection_names(market_id)
    except Exception:
        raise MarketNotFoundException(f"Market not found for market_id {market_id}.")

    market = betfair_client.get_market_book(market_id)

    runners = []
    for runner_book in market["runners"]:
        if runner_book["status"] != "ACTIVE":
            continue
        selection_id = runner_book["selectionId"]
        runner_name = runner_names[selection_id]
        runner = Runner(
            runner_id=selection_id,
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
    client: BetfairClient,
    request: SweepstakesRequest,
) -> db_models.Sweepstakes:
    selections = get_selections(client, request.market_id, request.ignore_longshots)
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
    )

    for participant_name, selections in sweepstake_assignments.items():
        participant_db = db_models.Participant(
            name=participant_name,
            equity=Decimal(0),
            sweepstake=sweepstakes_db,
            runners=[],
        )

        sorted_selections = sorted(
            selections, key=lambda x: x.implied_probability, reverse=True
        )

        participant_db.runners = [
            db_models.Runner(
                name=selection.name,
                probability=selection.implied_probability,
                provider_id=selection.provider_id,
                participant=participant_db,
            )
            for selection in sorted_selections
        ]

        for selection in sorted_selections:
            participant_db.equity += selection.implied_probability

        sweepstakes_db.participants.append(participant_db)

    return sweepstakes_db


def convert_db_model_to_response(
    sweepstakes_db: db_models.Sweepstakes,
) -> Sweepstakes:
    """
    Convert the database model to the API model.
    """

    jsondata = sweepstakes_db.model_dump()
    participants = [
        {
            "name": participant.name,
            "equity": participant.equity,
            "assignments": [
                {
                    "provider_id": runner.provider_id,
                    "name": runner.name,
                    "implied_probability": runner.probability,
                }
                for runner in participant.runners
            ],
        }
        for participant in sweepstakes_db.participants
    ]

    jsondata["participants"] = participants

    return Sweepstakes(**jsondata)
