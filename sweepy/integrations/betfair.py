import requests


LOGIN_URL = "https://identitysso.betfair.com/api/login"


class BetfairClient:
    BASE_SPORTS_URL = "https://api.betfair.com/exchange/betting/rest/v1.0/"

    def __init__(self, username: str, password: str, app_key: str) -> None:
        self.username = username
        self.password = password
        self.app_key = app_key
        self.token = self._login()

    def __headers(self, include_token: bool = True):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Application": self.app_key,
        }
        if include_token:
            headers["X-Authentication"] = self.token
        return headers

    def _login(self):
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
