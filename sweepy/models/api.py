from pydantic import BaseModel, conlist

from sweepy.models.enums import AssignmentMethod

from .participant import Participant


class SweepstakesRequest(BaseModel):
    """
    Model for the request to create a new sweepstakes.
    """

    name: str
    market_id: str
    method: AssignmentMethod
    participant_names: list[str] = conlist(str, min_length=2)
    ignore_longshots: bool = False


class SweepstakesResponse(BaseModel):
    """
    Model for the response from the API after creating a new sweepstakes.
    """

    name: str
    market_id: str
    method: AssignmentMethod
    num_selections: int
    participants: list[Participant]

    def __str__(self):
        sep = "\n\n"
        return f"Name: {self.name}\nMarket ID: {self.market_id}\nMethod: {self.method.value}\nNo. of Selections: {self.num_selections}\nNo. Of Participants: {len(self.participants)}\nAssignments:{sep}{sep.join([str(participant) for participant in self.participants])}"
