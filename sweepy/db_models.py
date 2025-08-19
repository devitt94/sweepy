import datetime
from hashids import Hashids
from typing import List, Optional
from sqlmodel import Column, DateTime, SQLModel, Field, Relationship

hashids = Hashids(
    min_length=4, salt="sweepy_salt", alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
)


class Sweepstakes(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    market_id: str
    competition: str
    method: str
    active: bool
    start_date: datetime.datetime = Field(
        sa_column=Column(DateTime(timezone=True)),
    )
    updated_at: datetime.datetime = Field(
        sa_column=Column(DateTime(timezone=True)),
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
    )
    participants: List["Participant"] = Relationship(back_populates="sweepstake")
    tournament_id: Optional[str] = None

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

    @property
    def runners(self) -> List["Runner"]:
        """
        Returns the list of runners associated with the sweepstake.
        """
        return [
            runner
            for participant in self.participants
            for runner in participant.runners
        ]

    @property
    def has_leaderboard(self) -> bool:
        """
        Returns whether the sweepstake has score data.
        """
        return self.tournament_id is not None


class Participant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    sweepstake_id: Optional[int] = Field(default=None, foreign_key="sweepstakes.id")

    sweepstake: Optional["Sweepstakes"] = Relationship(back_populates="participants")
    runners: List["Runner"] = Relationship(back_populates="participant")
    odds_history: List["ParticipantOdds"] = Relationship(
        back_populates="participant",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )

    @property
    def latest_odds(self) -> Optional["ParticipantOdds"]:
        """
        Returns the most recent odds for the participant.
        """
        if self.odds_history:
            return max(self.odds_history, key=lambda odds: odds.timestamp)
        return None


class ParticipantOdds(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    participant_id: Optional[int] = Field(default=None, foreign_key="participant.id")
    implied_probability: float
    timestamp: datetime.datetime = Field(
        sa_column=Column(DateTime(timezone=True)),
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
    )

    participant: Optional["Participant"] = Relationship(back_populates="odds_history")


class Runner(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    market_provider_id: str
    score_provider_id: Optional[str] = None
    score: Optional[int] = None
    participant_id: Optional[int] = Field(default=None, foreign_key="participant.id")

    participant: Optional["Participant"] = Relationship(back_populates="runners")

    odds_history: List["RunnerOdds"] = Relationship(
        back_populates="runner",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )

    @property
    def latest_odds(self) -> Optional["RunnerOdds"]:
        """
        Returns the most recent odds for the runner.
        """
        if self.odds_history:
            return max(self.odds_history, key=lambda odds: odds.timestamp)
        return None


class RunnerOdds(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    runner_id: Optional[int] = Field(default=None, foreign_key="runner.id")
    implied_probability: float
    timestamp: datetime.datetime = Field(
        sa_column=Column(DateTime(timezone=True)),
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
    )

    runner: Optional["Runner"] = Relationship(back_populates="odds_history")
