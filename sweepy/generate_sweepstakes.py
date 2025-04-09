from decimal import Decimal
import random
from sweepy.calculator import compute_market_probabilities
from sweepy.cli import AssignmentMethod
from sweepy.integrations.betfair import BetfairClient
from sweepy.models import Runner, RunnerOdds
from sweepy import assignment
from sweepy.models.api import SweepstakesResponse
from sweepy.models.participant import Participant


def get_selections(
    betfair_client: BetfairClient, market_id: str, ignore_longshots: bool
) -> list[RunnerOdds]:
    runner_names = betfair_client.get_selection_names(market_id)

    market = betfair_client.get_market_book(market_id)

    runners = []
    for runner_book in market["runners"]:
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
    market_id: str,
    participants: list[str],
    method: AssignmentMethod,
    ignore_longshots: bool = False,
) -> SweepstakesResponse:
    selections = get_selections(client, market_id, ignore_longshots)
    num_selections = len(selections)

    selection_assigner_func: callable[
        [list[str], list[RunnerOdds]], dict[str, list[RunnerOdds]]
    ]

    if method == AssignmentMethod.STAGGERED:
        selection_assigner_func = assignment.assign_selections_staggered
    elif method == AssignmentMethod.TIERED:
        selection_assigner_func = assignment.assign_selections_tiered
    elif method == AssignmentMethod.RANDOM:
        selection_assigner_func = assignment.assign_selections_random
    elif method == AssignmentMethod.FAIR:
        selection_assigner_func = assignment.assign_selections_fair
    else:
        raise NotImplementedError(f"Assignment method {method} not implemented")

    random.shuffle(participants)
    sweepstake_assignments: dict[str, list[RunnerOdds]] = selection_assigner_func(
        participants=participants,
        selections=selections,
    )

    assigned_participants = []

    for participant_name, selections in sweepstake_assignments.items():
        participant_equity = Decimal(0)

        sorted_selections = sorted(
            selections, key=lambda x: x.implied_probability, reverse=True
        )
        for selection in sorted_selections:
            participant_equity += selection.implied_probability

        assigned_participants.append(
            Participant(
                name=participant_name,
                assignments=sorted_selections,
                equity=participant_equity,
            )
        )

    return SweepstakesResponse(
        name="Sweepstakes " + market_id,
        market_id=market_id,
        method=method,
        num_selections=num_selections,
        participants=assigned_participants,
    )
