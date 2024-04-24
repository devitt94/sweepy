import os
import dotenv
import random
from sweepy.assignment import assign_selections_tiered
from sweepy.integrations.betfair import BetfairClient
from sweepy.models.market import Market
from sweepy.calculator import compute_market_probabilities
from sweepy.models.runner import Runner
from sweepy.models.runner_probability import RunnerProbability


US_PRESEDENTIAL_ELECTION = "1.176878927"
US_OPEN_GOLF_WINNER = "1.216450255"


PARTICIPANTS = [
    "Alice",
    "Bob",
    "Charlie",
    "David",
    "Edward",
    "Frank",
    "Geoff",
    "Harry",
    "India",
    "Jade",
    "Katherine",
    "Laura",
    "Mark",
    "Nick",
    "Olivia",
    "Peter",
    "Quentin",
    "Rory",
    "Stephen",
    "Tom",
    "Ulrich",
    "Victoria",
]


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

    market = Market(
        market_id=market_id,
        market_name="US Open Golf Winner",
        market_status="OPEN",
        runners=runners,
    )

    return compute_market_probabilities(market)


def main():
    dotenv.load_dotenv()
    client = BetfairClient(
        username=os.getenv("BETFAIR_USERNAME"),
        password=os.getenv("BETFAIR_PASSWORD"),
        app_key=os.getenv("BETFAIR_APP_KEY"),
    )

    selections = get_selections(client, US_OPEN_GOLF_WINNER)

    num_participants = 10
    participants = PARTICIPANTS[:num_participants].copy()
    random.shuffle(participants)
    sweepstake_assignments = assign_selections_tiered(
        participants=participants,
        selections=selections,
    )

    for k, selections in sweepstake_assignments.items():
        print(k, round(sum(sel.market_adjusted for sel in selections), 3))


if __name__ == "__main__":
    main()
