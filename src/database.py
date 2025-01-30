from sqlmodel import SQLModel, create_engine, Session
from models import Movie


# Harcoded postgres for now - this should be in config
engine = create_engine(
    "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"
)

SQLModel.metadata.create_all(engine)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
