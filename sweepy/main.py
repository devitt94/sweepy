from decimal import Decimal
from enum import Enum
import os
import dotenv
import random

import typer
from sweepy.assignment import (
    assign_selections_fair,
    assign_selections_random,
    assign_selections_staggered,
    assign_selections_tiered,
)
from sweepy.integrations.betfair import BetfairClient
from sweepy.calculator import compute_market_probabilities
from sweepy.models.runner import Runner
from sweepy.models.runner_probability import RunnerProbability


app = typer.Typer()
dotenv.load_dotenv()


class AssignmentMethod(str, Enum):
    STAGGERED = "staggered"
    TIERED = "tiered"
    RANDOM = "random"
    FAIR = "fair"


def get_selections(
    betfair_client: BetfairClient, market_id: str
) -> list[RunnerProbability]:
    runner_names = betfair_client.get_selection_names(market_id)

    market = betfair_client.get_market_book(market_id)

    runners = []
    for runner_book in market["runners"]:
        selection_id = runner_book["selectionId"]
        runner_name = runner_names[selection_id]
        runners.append(
            Runner(
                runner_id=selection_id,
                name=runner_name,
                available_to_back=runner_book["ex"]["availableToBack"],
                available_to_lay=runner_book["ex"]["availableToLay"],
                last_price_traded=runner_book.get("lastPriceTraded"),
            )
        )

    return compute_market_probabilities(runners)


@app.command()
def generate_sweepstakes(
    market_id: str = typer.Argument(
        ..., help="The betfair market ID to generate the sweepstakes for"
    ),
    participants: list[str] = typer.Argument(
        ..., help="The participants in the sweepstakes"
    ),
    method: AssignmentMethod = typer.Option(
        AssignmentMethod.TIERED,
        case_sensitive=False,
        help="The method to use to assign selections to participants",
    ),
):
    client = BetfairClient(
        username=os.getenv("BETFAIR_USERNAME"),
        password=os.getenv("BETFAIR_PASSWORD"),
        app_key=os.getenv("BETFAIR_APP_KEY"),
    )

    selections = get_selections(client, market_id)

    selection_assigner_func: callable[
        [list[str], list[RunnerProbability]], dict[str, list[RunnerProbability]]
    ]
    if method == AssignmentMethod.STAGGERED:
        selection_assigner_func = assign_selections_staggered
    elif method == AssignmentMethod.TIERED:
        selection_assigner_func = assign_selections_tiered
    elif method == AssignmentMethod.RANDOM:
        selection_assigner_func = assign_selections_random
    elif method == AssignmentMethod.FAIR:
        selection_assigner_func = assign_selections_fair
    else:
        raise NotImplementedError(f"Assignment method {method} not implemented")

    random.shuffle(participants)
    sweepstake_assignments: dict[str, list[RunnerProbability]] = (
        selection_assigner_func(
            participants=participants,
            selections=selections,
        )
    )

    for participant, selections in sweepstake_assignments.items():
        s = ""
        participant_probability = Decimal(0)
        for selection in sorted(
            selections, key=lambda x: x.market_adjusted, reverse=True
        ):
            participant_probability += selection.market_adjusted
            s += f"\t{selection.runner.name} ({selection.market_adjusted*100:.2f}%)\n"

        print(f"{participant}: {participant_probability*100:.2f}%")
        print(s)


if __name__ == "__main__":
    app()
