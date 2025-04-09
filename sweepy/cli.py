import os
import dotenv

import typer
from sweepy import generate_sweepstakes
from sweepy.integrations.betfair import BetfairClient
from sweepy.models.enums import AssignmentMethod


app = typer.Typer()
dotenv.load_dotenv()


@app.command()
def generate_sweepstakes_cli(
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

    response = generate_sweepstakes.generate_sweepstakes(
        client=client,
        market_id=market_id,
        participants=participants,
        method=method,
    )

    print(response)


if __name__ == "__main__":
    app()
