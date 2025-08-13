import datetime
from pydantic import BaseModel


class Tournament(BaseModel):
    id: str
    name: str
    start_date: datetime.date
