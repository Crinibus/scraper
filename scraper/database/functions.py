from sqlmodel import Session, select, col

from scraper.models.product import ProductInfo
from .db import engine
from .models import Product, DataPoint


def delete_all(elements: list[Product | DataPoint]) -> None:
    with Session(engine) as session:
        for element in elements:
            session.delete(element)
        session.commit()


def add(element: Product | DataPoint) -> None:
    with Session(engine) as session:
        session.add(element)
        session.commit()


def add_all(elements: list[Product] | list[DataPoint]) -> None:
    with Session(engine) as session:
        session.add_all(elements)
        session.commit()


def get_all_products() -> list[Product]:
    with Session(engine) as session:
        return session.exec(select(Product)).all()


def get_all_datapoints() -> list[DataPoint]:
    with Session(engine) as session:
        return session.exec(select(DataPoint)).all()


def get_all_unique_categories() -> list[str]:
    with Session(engine) as session:
        return session.exec(select(Product.category).distinct()).all()


def get_all_unique_domains() -> list[str]:
    with Session(engine) as session:
        return session.exec(select(Product.domain).distinct()).all()


def get_all_active_products() -> list[Product]:
    with Session(engine) as session:
        return session.exec(select(Product).where(Product.isActive)).all()


def get_product_by_product_code(product_code: str) -> Product | None:
    with Session(engine) as session:
        return session.exec(select(Product).where(Product.product_code == product_code)).first()


def get_products_by_product_codes(product_codes: list[str]) -> list[Product]:
    with Session(engine) as session:
        return session.exec(select(Product).where(col(Product.product_code).in_(product_codes))).all()


def get_products_by_categories(categories: list[str]) -> list[Product]:
    with Session(engine) as session:
        return session.exec(select(Product).where(col(Product.category).in_(categories))).all()


def get_products_by_names(names: list[str]) -> list[Product]:
    with Session(engine) as session:
        return session.exec(select(Product).where(col(Product.name).in_(names))).all()


def get_products_by_names_fuzzy(names: list[str]) -> list[Product]:
    with Session(engine) as session:
        matched_products = []

        for name in names:
            name = f"%{name}%"
            products = session.exec(select(Product).where(col(Product.name).like(name))).all()
            matched_products.extend(products)

        return matched_products


def get_products_by_domains(domains: list[str], select_only_active: bool = False) -> list[Product]:
    with Session(engine) as session:
        query = select(Product).where(col(Product.domain).in_(domains))

        if select_only_active:
            query = query.where(Product.isActive)

        return session.exec(query).all()


def get_datapoints_by_categories(categories: list[str]) -> list[DataPoint]:
    with Session(engine) as session:
        products = session.exec(select(Product).where(col(Product.category).in_(categories))).all()
        product_codes = [product.product_code for product in products]
        datapoints = session.exec(select(DataPoint).where(col(DataPoint.product_code).in_(product_codes))).all()
        return datapoints


def get_datapoints_by_names(names: list[str]) -> list[DataPoint]:
    with Session(engine) as session:
        products = session.exec(select(Product).where(col(Product.name).in_(names))).all()
        product_codes = [product.product_code for product in products]
        datapoints = session.exec(select(DataPoint).where(col(DataPoint.product_code).in_(product_codes))).all()
        return datapoints


def get_datapoints_by_product_codes(product_codes: list[str]) -> list[DataPoint]:
    with Session(engine) as session:
        products = session.exec(select(Product).where(col(Product.product_code).in_(product_codes))).all()
        found_product_codes = [product.product_code for product in products]
        datapoints = session.exec(select(DataPoint).where(col(DataPoint.product_code).in_(found_product_codes))).all()
        return datapoints


def get_all_products_with_datapoints() -> list[ProductInfo]:
    products = get_all_products()
    return get_product_infos_from_products(products)


def get_product_infos_from_products(products: list[Product]) -> list[ProductInfo]:
    with Session(engine) as session:
        product_infos: list[ProductInfo] = []

        for product in products:
            datapoints = session.exec(
                select(DataPoint).where(DataPoint.product_code == product.product_code).order_by(DataPoint.date)
            ).all()

            product_info = ProductInfo(
                id=product.product_code,
                product_name=product.name,
                category=product.category,
                currency=datapoints[0].currency,
                datapoints=datapoints,
                url=product.url,
                website=product.domain,
            )

            product_infos.append(product_info)

        return product_infos


def get_all_products_grouped_by_domains(select_only_active: bool = False) -> list[list[Product]]:
    grouped_products = []

    unique_domains = get_all_unique_domains()

    for domain in unique_domains:
        products = get_products_by_domains([domain], select_only_active=select_only_active)

        if not products:
            continue

        grouped_products.append(products)

    return grouped_products
