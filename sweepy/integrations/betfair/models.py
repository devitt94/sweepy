from datetime import datetime
from pydantic import BaseModel

GOLF_EVENT_TYPE_ID = 3


class MarketInfo(BaseModel):
    """
    Model for market information.
    """

    market_id: str
    market_name: str
    event_type: int
    event_name: str
    competition_name: str
    market_start_time: datetime

    model_config = {"frozen": True}

    def __eq__(self, other: "MarketInfo") -> bool:
        if not isinstance(other, MarketInfo):
            return NotImplemented

        return self.market_id == other.market_id

    @property
    def is_golf(self) -> bool:
        """
        Determines if the market is related to golf.
        """
        return self.event_type == GOLF_EVENT_TYPE_ID
