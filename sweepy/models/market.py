from decimal import Decimal
from pydantic import BaseModel, condecimal


class PriceSize(BaseModel):
    price: Decimal = condecimal(ge=1, le=1000)
    size: Decimal = condecimal(ge=0, le=1000)


class Runner(BaseModel):
    runner_id: str
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


class Market(BaseModel):
    market_id: str
    market_name: str
    market_status: str
    runners: list[Runner]
