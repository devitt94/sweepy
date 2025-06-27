import datetime
from pydantic import BaseModel, condecimal
from decimal import Decimal

from sweepy.models.enums import AssignmentMethod


class RunnerOdds(BaseModel):
    provider_id: str
    name: str
    implied_probability: Decimal = condecimal(ge=0, le=1)

    def __le__(self, other: "RunnerOdds") -> bool:
        return self.implied_probability <= other.implied_probability

    def __gt__(self, other: "RunnerOdds") -> bool:
        return self.implied_probability > other.implied_probability

    def __str__(self):
        return f"{self.name} ({self.implied_probability*100:.2f}%)"

    class Config:
        frozen = True


class Participant(BaseModel):
    """
    Model for a participant in a sweepstakes.
    """

    name: str
    equity: Decimal
    assignments: list[RunnerOdds]

    def __str__(self):
        separator = "\n\t"
        return f"{self.name} ({self.equity*100:.2f}%){separator}{separator.join([str(assignment) for assignment in self.assignments])}"


class Sweepstakes(BaseModel):
    id: str
    name: str
    market_id: str
    method: AssignmentMethod
    updated_at: datetime.datetime
    participants: list[Participant]
    active: bool
    ignore_longshots: bool = False
    competition: str | None = None
