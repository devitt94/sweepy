import requests
from datetime import datetime

from sweepy.cache import timed_cache

from .models import Tournament


BASE_URL = "https://live-golf-data.p.rapidapi.com/"


def parse_tournament_from_schedule_response(tournament_data: dict) -> Tournament:
    """
    Parses a tournament from the schedule data.
    """

    tournament_id = tournament_data["tournId"]
    name = tournament_data["name"]
    start_date = datetime.fromtimestamp(
        int(tournament_data["date"]["start"]["$date"]["$numberLong"]) // 1000
    ).date()

    return Tournament(
        id=tournament_id,
        name=name,
        start_date=start_date,
    )


class LiveGolfClient:
    def __init__(self, api_key: str):
        self.api_key = api_key

    @property
    def __headers(self):
        return {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "live-golf-data.p.rapidapi.com",
            "Content-Type": "application/json",
        }

    def get_schedule(self, season: int, tour_id: int = 1) -> list[Tournament]:
        url = f"{BASE_URL}schedule"
        response = requests.get(
            url, headers=self.__headers, params={"orgId": tour_id, "year": season}
        )
        response.raise_for_status()
        schedule = response.json()["schedule"]
        return list(map(parse_tournament_from_schedule_response, schedule))

    @timed_cache(60)
    def get_leaderboard(self, year: int, tournament_id: str, tour_id: int = 1):
        url = f"{BASE_URL}leaderboard"
        response = requests.get(
            url,
            headers=self.__headers,
            params={"orgId": tour_id, "year": year, "tournId": tournament_id},
        )
        response.raise_for_status()
        return response.json()
