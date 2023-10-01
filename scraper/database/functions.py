from sqlmodel import Session, select, col
from .db import engine
from .models import Product, DataPoint


def delete_all(elements: list[Product | DataPoint]) -> None:
    with Session(engine) as session:
        for element in elements:
            session.delete(element)
        session.commit()


def get_all_products() -> list[Product]:
    with Session(engine) as session:
        return session.exec(select(Product)).all()


def get_all_datapoints() -> list[DataPoint]:
    with Session(engine) as session:
        return session.exec(select(DataPoint)).all()


def get_product_by_product_code(product_code: str) -> Product | None:
    with Session(engine) as session:
        return session.exec(select(Product).where(Product.product_code == product_code)).first()


def get_products_by_product_codes(product_codes: list[str]) -> list[Product]:
    with Session(engine) as session:
        return session.exec(select(col(Product.product_code).in_(product_codes))).all()


def get_products_by_categories(categories: list[str]) -> list[Product]:
    with Session(engine) as session:
        return session.exec(select(col(Product.category).in_(categories))).all()


def get_products_by_names(names: list[str]) -> list[Product]:
    with Session(engine) as session:
        return session.exec(select(col(Product.name).in_(names))).all()


def add_product(product: Product) -> None:
    with Session(engine) as session:
        session.add(product)
        session.commit()


def add_datapoint(datapoint: DataPoint) -> None:
    with Session(engine) as session:
        session.add(datapoint)
        session.commit()
