from sqlmodel import SQLModel, create_engine
from scraper.filemanager import Filemanager
from .models import Product, DataPoint  # noqa: F401

sqlite_url = f"sqlite:///{Filemanager.database_path}"

engine = create_engine(sqlite_url, echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
