from sqlmodel import SQLModel, create_engine
from .models import Product, DataPoint  # noqa: F401

sqlite_file_name = "database/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
