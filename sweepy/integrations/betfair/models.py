from datetime import datetime
from pydantic import BaseModel


class MarketInfo(BaseModel):
    """
    Model for market information.
    """

    market_id: str
    market_name: str
    event_name: str
    competition_name: str
    market_start_time: datetime

    model_config = {"frozen": True}
