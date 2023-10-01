import logging
import scraper.database as db


def delete(categories: list[str], names: list[str], product_codes: list[str], all: bool) -> None:
    print("Deleting...")
    logging.getLogger(__name__).info(f"Deleting products and datapoint for {categories=}, {names=}, {product_codes=}, {all=}")

    if all:
        delete_all()
        return

    if categories:
        delete_products_by_categories(categories)

    if names:
        delete_products_by_names(names)

    if product_codes:
        delete_products_by_product_codes(product_codes)


def delete_all() -> None:
    print("Deleting all products and datapoints...")
    logging.getLogger(__name__).info("Deleting all products and datapoints")

    all_products = db.get_all_products()
    all_datapoints = db.get_all_datapoints()

    db.delete_all(all_products)
    db.delete_all(all_datapoints)


def delete_products_by_categories(categories: list[str]) -> None:
    products = db.get_products_by_categories(categories)
    db.delete_all(products)


def delete_products_by_names(names: list[str]) -> None:
    products = db.get_products_by_names(names)
    db.delete_all(products)


def delete_products_by_product_codes(product_codes: list[str]) -> None:
    products = db.get_products_by_product_codes(product_codes)
    db.delete_all(products)
