import logging
import rapidfuzz
from sqlmodel import Session

from sweepy import db_models
from sweepy.integrations.live_golf import LiveGolfClient, Tournament
from sweepy.integrations.betfair import MarketInfo


START_DAY_DIFF_THRESHOLD = 1
NAME_MATCH_RATIO_THRESHOLD = 65


def get_live_golf_tournament(
    bf_info: MarketInfo,
    live_golf_client: LiveGolfClient,
) -> Tournament:
    """
    Finds the corresponding Live Golf tournament ID for a given Betfair market ID.
    """

    try:
        lg_schedule = live_golf_client.get_schedule(
            season=bf_info.market_start_time.year
        )
    except Exception as e:
        raise ValueError(f"Error fetching Live Golf schedule: {e}")

    for tournament in lg_schedule:
        name_match_ratio = rapidfuzz.fuzz.ratio(tournament.name, bf_info.event_name)

        date_match = (tournament.start_date - bf_info.market_start_time.date()).days
        if (
            abs(date_match) <= START_DAY_DIFF_THRESHOLD
            and name_match_ratio >= NAME_MATCH_RATIO_THRESHOLD
        ):
            return tournament

    raise ValueError(
        f"No matching Live Golf tournament found for Betfair market ID {bf_info}. "
        f"Event name: {bf_info.event_name}, Start date: {bf_info.market_start_time.date()}"
    )


def match_runners_to_live_golf(
    runners: list[db_models.Runner],
    lg_tournament_id: str,
    season: int,
    lg_client: LiveGolfClient,
    session: Session,
) -> None:
    """
    Matches Betfair runners to Live Golf runners for a specific tournament.
    """

    leaderboard = lg_client.get_leaderboard(season, lg_tournament_id)

    unmatched_runners = {runner.name: runner for runner in runners}
    runners_matched = 0

    for player in leaderboard["leaderboardRows"]:
        lg_player_name = f"{player['firstName']} {player['lastName']}"
        lg_id = player["playerId"]

        if lg_player_name in unmatched_runners:
            runner = unmatched_runners.pop(lg_player_name)
            runner.score_provider_id = lg_id
            session.add(runner)
            runners_matched += 1
        else:
            logging.warning(
                f"No Betfair runner matched for Live Golf player '{lg_player_name}' with ID {lg_id}."
            )

    logging.info(
        f"Total runners matched: {runners_matched} / {len(leaderboard['leaderboardRows'])}"
    )
    session.commit()
