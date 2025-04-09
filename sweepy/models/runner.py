from decimal import Decimal
from pydantic import BaseModel

from .price_size import PriceSize


class Runner(BaseModel):
    runner_id: int
    name: str
    available_to_back: list[PriceSize]
    available_to_lay: list[PriceSize]
    last_price_traded: Decimal | None = None

    @property
    def best_back_price(self) -> Decimal:
        try:
            return self.available_to_back[0].price
        except IndexError:
            return Decimal("nan")

    @property
    def best_lay_price(self) -> Decimal:
        try:
            return self.available_to_lay[0].price
        except IndexError:
            return Decimal("nan")
