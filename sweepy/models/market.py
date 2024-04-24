from pydantic import BaseModel

from sweepy.models.runner import Runner


class Market(BaseModel):
    market_id: str
    market_name: str
    market_status: str
    runners: list[Runner]
