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
    isActive: bool


class DataPoint(SQLModel, table=True):
    __tablename__: str = "datapoints"

    id: int = Field(default=None, primary_key=True)
    product_code: str
    date: str
    price: float
    currency: str
