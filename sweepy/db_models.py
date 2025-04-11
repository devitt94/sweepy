from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class Participant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    equity: float
    sweepstake_id: Optional[int] = Field(default=None, foreign_key="sweepstakes.id")
    runners: List["Runner"] = Relationship(back_populates="participant")

    sweepstake: Optional["Sweepstakes"] = Relationship(back_populates="participants")


class Sweepstakes(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    market_id: str
    method: str
    num_selections: int

    participants: List[Participant] = Relationship(back_populates="sweepstake")


class Runner(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    probability: float
    participant_id: Optional[int] = Field(default=None, foreign_key="participant.id")
