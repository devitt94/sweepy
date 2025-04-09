from pydantic import BaseModel
from decimal import Decimal

from .runner_odds import RunnerOdds


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
