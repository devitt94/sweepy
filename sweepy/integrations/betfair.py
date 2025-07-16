import logging
import requests
from sweepy.cache import timed_cached_property

LOGIN_URL = "https://identitysso.betfair.com/api/login"


class BetfairClient:
    BASE_SPORTS_URL = "https://api.betfair.com/exchange/betting/rest/v1.0/"

    def __init__(self, username: str, password: str, app_key: str) -> None:
        self.username = username
        self.password = password
        self.app_key = app_key

    def __headers(self, include_token: bool = True):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Application": self.app_key,
        }
        if include_token:
            headers["X-Authentication"] = self.token
        return headers

    @timed_cached_property(ttl_seconds=1800)
    def token(self):
        logging.info("Fetching Betfair API token.")
        response = requests.post(
            LOGIN_URL,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
                "X-Application": self.app_key,
            },
            data={
                "username": self.username,
                "password": self.password,
            },
        )
        response.raise_for_status()
        response_data = response.json()
        return response_data["token"]

    def get_selection_names(self, market_id: str):
        url = f"{self.BASE_SPORTS_URL}listMarketCatalogue/"
        response = requests.post(
            url,
            headers=self.__headers(),
            json={
                "filter": {
                    "marketIds": [market_id],
                },
                "maxResults": 1000,
                "marketProjection": ["RUNNER_DESCRIPTION"],
            },
        )
        response.raise_for_status()
        response_data = response.json()
        runners = {
            runner["selectionId"]: runner["runnerName"]
            for runner in response_data[0]["runners"]
        }
        return runners

    def get_market_book(self, market_id: str):
        url = f"{self.BASE_SPORTS_URL}listMarketBook/"
        response = requests.post(
            url,
            headers=self.__headers(),
            json={
                "marketIds": [market_id],
                "priceProjection": {
                    "priceData": ["EX_BEST_OFFERS"],
                },
            },
        )

        response.raise_for_status()
        response_data = response.json()
        return response_data[0]

    def get_event_types(self) -> list[dict]:
        url = f"{self.BASE_SPORTS_URL}listEventTypes/"
        response = requests.post(
            url,
            headers=self.__headers(),
            json={
                "filter": {},
                "maxResults": 100,
            },
        )
        response.raise_for_status()

        return [item["eventType"] for item in response.json()]

    def get_outright_markets(self, event_type_id: str) -> list[dict]:
        url = f"{self.BASE_SPORTS_URL}listMarketCatalogue/"
        response = requests.post(
            url,
            headers=self.__headers(),
            json={
                "filter": {
                    "eventTypeIds": [event_type_id],
                    "marketTypeCodes": [
                        "WINNER",
                        "TOURNAMENT_WINNER",
                        "OUTRIGHT_WINNER",
                        "NONSPORT",
                    ],
                },
                "maxResults": 25,
                "marketProjection": ["EVENT", "COMPETITION"],
                "sort": "FIRST_TO_START",
            },
        )
        response.raise_for_status()

        return [
            {
                "market_id": market["marketId"],
                "market_name": market["marketName"],
                "event_name": market["event"]["name"],
                "competition_name": market["competition"]["name"],
            }
            for market in response.json()
            if "event" in market and "competition" in market
        ]
