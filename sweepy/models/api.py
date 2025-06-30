from pydantic import BaseModel, conlist

from sweepy.models.enums import AssignmentMethod


class SweepstakesRequest(BaseModel):
    """
    Model for the request to create a new sweepstakes.
    """

    name: str
    market_id: str
    method: AssignmentMethod
    participant_names: conlist(str, min_length=2)
    competition: str | None = None
    ignore_longshots: bool = False


class EventType(BaseModel, frozen=True):
    """
    Model for the event type in the Betfair API.
    """

    id: str
    name: str


class MarketInfo(BaseModel, frozen=True):
    """
    Model for the market information in the Betfair API.

    """

    market_id: str
    market_name: str
    event_name: str
    competition_name: str

    def __eq__(self, other: "MarketInfo") -> bool:
        if not isinstance(other, MarketInfo):
            return NotImplemented

        return self.market_id == other.market_id
