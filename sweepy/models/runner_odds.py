from pydantic import BaseModel, condecimal
from decimal import Decimal


class RunnerOdds(BaseModel):
    runner_name: str
    implied_probability: Decimal = condecimal(ge=0, le=1)

    def __le__(self, other: "RunnerOdds") -> bool:
        return self.implied_probability <= other.implied_probability

    def __gt__(self, other: "RunnerOdds") -> bool:
        return self.implied_probability > other.implied_probability

    def __str__(self):
        return f"{self.runner_name} ({self.implied_probability*100:.2f}%)"

    class Config:
        frozen = True
