from zipapp import create_archive
from sqlmodel import SQLModel, create_engine
from .core.config import settings
from sqlalchemy_utils import create_database, database_exists

DB_URL = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}"

engine = create_engine(DB_URL, echo=True)


def create_tabls():
    SQLModel.metadata.create_all(engine)


def database_create():
    if not database_exists(DB_URL):
        create_database(DB_URL)
