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
    log_product_codes_with_message(products, "Deleting products with categories")
    db.delete_all(products)


def delete_products_by_names(names: list[str]) -> None:
    products = db.get_products_by_names(names)
    log_product_codes_with_message(products, "Deleting products by names")
    db.delete_all(products)


def delete_products_by_product_codes(product_codes: list[str]) -> None:
    products = db.get_products_by_product_codes(product_codes)
    log_product_codes_with_message(products, "Deleting products with product codes")
    db.delete_all(products)


def log_product_codes_with_message(products: list[db.Product], log_message: str) -> None:
    logger = logging.getLogger(__name__)
    product_codes = [product.product_code for product in products]

    if product_codes:
        product_codes_string = ", ".join(product_codes)
        print(f"Deleting product codes: {product_codes_string}")
    else:
        print("No product found to delete")

    logger.info(f"{log_message} - {product_codes=}")
