import rapidfuzz

from sweepy.integrations.betfair import BetfairClient
from sweepy.integrations.live_golf import LiveGolfClient


START_DAY_DIFF_THRESHOLD = 1
NAME_MATCH_RATIO_THRESHOLD = 75


def get_live_golf_tournament_id(
    betfair_market_id: str,
    betfair_client: BetfairClient,
    live_golf_client: LiveGolfClient,
) -> str:
    """
    Finds the corresponding Live Golf tournament ID for a given Betfair market ID.
    """

    bf_info = betfair_client.get_market_info(betfair_market_id)

    print(f"Betfair Market Info: {bf_info}")
    lg_schedule = live_golf_client.get_schedule(season=bf_info.market_start_time.year)

    for tournament in lg_schedule:
        name_match_ratio = rapidfuzz.fuzz.ratio(tournament.name, bf_info.event_name)

        date_match = (tournament.start_date - bf_info.market_start_time.date()).days
        if (
            abs(date_match) <= START_DAY_DIFF_THRESHOLD
            and name_match_ratio >= NAME_MATCH_RATIO_THRESHOLD
        ):
            print(f"Found matching tournament: {tournament.name} (ID: {tournament.id})")
            return tournament.id

    raise ValueError(
        f"No matching Live Golf tournament found for Betfair market ID {betfair_market_id}. "
        f"Event name: {bf_info.event_name}, Start date: {bf_info.market_start_time.date()}"
    )
