import os
import dotenv

import typer
from sweepy import generate_sweepstakes
from sweepy.integrations.betfair import BetfairClient
from sweepy.models import AssignmentMethod, SweepstakesRequest


app = typer.Typer()
dotenv.load_dotenv()


@app.command()
def generate_sweepstakes_cli(
    name: str = typer.Argument(..., help="The name of the sweepstakes to generate"),
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
    ignore_longshots: bool = typer.Option(
        False,
        help="Exclude selections with odds greater than 1000 (i.e. not available to lay)",
    ),
):
    client = BetfairClient(
        username=os.getenv("BETFAIR_USERNAME"),
        password=os.getenv("BETFAIR_PASSWORD"),
        app_key=os.getenv("BETFAIR_APP_KEY"),
    )

    request = SweepstakesRequest(
        name=name,
        market_id=market_id,
        method=method,
        participant_names=participants,
        ignore_longshots=ignore_longshots,
    )

    response = generate_sweepstakes.generate_sweepstakes(
        client=client,
        request=request,
    )

    print(response)


if __name__ == "__main__":
    app()
