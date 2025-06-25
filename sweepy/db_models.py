import datetime
from hashids import Hashids
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

hashids = Hashids(
    min_length=4, salt="sweepy_salt", alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
)


class Sweepstakes(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    market_id: str
    method: str
    updated_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
    )
    participants: List["Participant"] = Relationship(back_populates="sweepstake")

    @property
    def stringified_id(self) -> Optional[str]:
        """
        Returns a stringified version of the sweepstake ID.
        """

        return f"S-{hashids.encode(self.id)}" if self.id is not None else None

    @staticmethod
    def decode_stringified_id(stringified_id: str) -> Optional[int]:
        """
        Decodes a stringified sweepstake ID back to an integer ID.
        """
        if not stringified_id.startswith("S-"):
            return None
        try:
            return hashids.decode(stringified_id[2:])[0]
        except IndexError:
            return None


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
