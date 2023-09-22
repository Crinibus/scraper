from sqlmodel import Session, select
from .db import engine
from .models import Product, DataPoint  # noqa: F401


def get_product_by_product_id(product_id: str) -> Product | None:
    with Session(engine) as session:
        return session.exec(select(Product).where(Product.productId == product_id)).first()
