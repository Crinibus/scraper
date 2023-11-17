import logging

import scraper.database as db


def reset(categories: list[str], names: list[str], product_codes: list[str], all: bool) -> None:
    print("Resetting datapoints...")
    logging.getLogger(__name__).info(f"Resetting datapoints for {categories=}, {names=}, {product_codes=}, {all=}")

    if all:
        delete_all_datapoints()
        return

    if categories:
        delete_datapoints_for_products_by_categories(categories)

    if names:
        delete_datapoints_for_products_by_names(names)

    if product_codes:
        delete_datapoints_for_products_by_product_codes(product_codes)


def delete_all_datapoints():
    datapoints = db.get_all_datapoints()
    db.delete_all(datapoints)


def delete_datapoints_for_products_by_categories(categories: list[str]):
    datapoints = db.get_datapoints_by_categories(categories)
    db.delete_all(datapoints)


def delete_datapoints_for_products_by_names(names: list[str]):
    datapoints = db.get_datapoints_by_names(names)
    db.delete_all(datapoints)


def delete_datapoints_for_products_by_product_codes(product_codes: list[str]):
    datapoints = db.get_datapoints_by_product_codes(product_codes)
    db.delete_all(datapoints)
