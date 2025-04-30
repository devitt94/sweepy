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
    ignore_longshots: bool = False
