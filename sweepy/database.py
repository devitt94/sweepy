from sqlmodel import SQLModel, create_engine, Session
import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if os.getenv("ENVIRONMENT") == "development":
    connect_args = {}
else:
    connect_args = {"sslmode": "require"}
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,  # Required for Heroku Postgres
)


def init_db():
    if os.getenv("ENVIRONMENT") == "development":
        SQLModel.metadata.drop_all(engine)

    SQLModel.metadata.create_all(engine)


def get_session():
    return Session(engine)
