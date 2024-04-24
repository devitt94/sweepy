from decimal import Decimal
from pydantic import BaseModel, condecimal


class PriceSize(BaseModel):
    price: Decimal = condecimal(ge=1, le=1000)
    size: Decimal = condecimal(ge=0, le=1000)
