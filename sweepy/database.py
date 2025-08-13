from sqlmodel import SQLModel, create_engine, Session
import os

from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DEV_MODE = os.getenv("ENVIRONMENT") == "development"

if DEV_MODE:
    connect_args = {}
else:
    connect_args = {"sslmode": "require"}
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,  # Required for Heroku Postgres
)


def init_db(recreate: bool = False):
    print(f"Initialising database: {DEV_MODE=} {DATABASE_URL=}")

    try:
        if recreate:
            SQLModel.metadata.drop_all(engine)
            print("Dropped existing database tables.")

        SQLModel.metadata.create_all(engine)
        print("Created database tables.")

    except Exception as e:
        print(f"Error initializing database: {e}")

    else:
        print("Database recreated.")


def get_session():
    return Session(engine)


if __name__ == "__main__":
    init_db()
