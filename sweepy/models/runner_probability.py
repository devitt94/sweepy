from pydantic import BaseModel, condecimal
from decimal import Decimal

from sweepy.models.runner import Runner


class RunnerProbability(BaseModel):
    runner: Runner
    market_adjusted: Decimal = condecimal(ge=0, le=1)
    implied: Decimal = condecimal(ge=0, le=1)

    def __le__(self, other: "RunnerProbability") -> bool:
        return self.implied <= other.implied

    def __gt__(self, other: "RunnerProbability") -> bool:
        return self.implied > other.implied
