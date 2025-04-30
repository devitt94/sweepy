from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship


class Sweepstakes(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    market_id: str
    method: str
    participants: List["Participant"] = Relationship(back_populates="sweepstake")


class Participant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    equity: float
    sweepstake_id: Optional[int] = Field(default=None, foreign_key="sweepstakes.id")

    sweepstake: Optional["Sweepstakes"] = Relationship(back_populates="participants")
    runners: List["Runner"] = Relationship(back_populates="participant")


class Runner(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    probability: float
    provider_id: str
    participant_id: Optional[int] = Field(default=None, foreign_key="participant.id")

    participant: Optional["Participant"] = Relationship(back_populates="runners")
