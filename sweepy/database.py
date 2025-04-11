from sqlmodel import SQLModel, create_engine, Session
import os

from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"},  # Required for Heroku Postgres
)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    return Session(engine)
