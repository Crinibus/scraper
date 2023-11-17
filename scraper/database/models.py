from datetime import datetime
from sqlmodel import Field, SQLModel


class Product(SQLModel, table=True):
    __tablename__: str = "products"

    id: int = Field(default=None, primary_key=True)
    product_code: str
    name: str
    category: str
    domain: str
    url: str
    short_url: str
    is_active: bool
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class DataPoint(SQLModel, table=True):
    __tablename__: str = "datapoints"

    id: int = Field(default=None, primary_key=True)
    product_code: str
    date: str
    price: float
    currency: str
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
