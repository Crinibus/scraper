import logging
from datetime import datetime

import scraper.database as db
from scraper.exceptions import WebsiteNotSupported, URLMissingSchema
from scraper.format import Format
from scraper.scrape import Scraper
from scraper.domains import get_website_name, SUPPORTED_DOMAINS
from scraper.constants import URL_SCHEMES


def add_products(categories: list[str], urls: list[str]) -> None:
    for category, url in zip(categories, urls):
        try:
            add_product(category, url)
        except (WebsiteNotSupported, URLMissingSchema) as err:
            logging.getLogger(__name__).error(err)
            print(err)


def add_product(category: str, url: str) -> None:
    logger = logging.getLogger(__name__)

    website_name = get_website_name(url, keep_subdomain=False)

    if website_name not in SUPPORTED_DOMAINS.keys():
        raise WebsiteNotSupported(website_name)

    if is_missing_url_schema(url):
        raise URLMissingSchema(url)

    print(f"Adding product with category '{category}' and url '{url}'")
    logger.info(f"Adding product with category '{category}' and url '{url}'")

    new_product = Scraper(category, url)
    new_product_info = new_product.scrape_info()

    if not new_product_info.valid:
        print("Product info is not valid - see logs for more info")
        return

    product_in_db = db.get_product_by_product_code(new_product_info.id)

    if product_in_db is None:
        add_new_product_to_db(new_product)
        add_new_datapoint_with_scraper(new_product)
        return

    logger.info("Product with the same product code already exists in database")

    if product_in_db.is_active:
        print("Product with the same product code already exists in database and is active")
        return

    user_input = input(
        "A product with the same product id already exist in the database but is not active, "
        "do you want to activate it? (y/n) > "
    )

    if user_input.lower() in ("y", "yes"):
        print("Activating product...")
        set_existing_product_is_active(product_in_db, True)
        logger.info("Product has been activated")
    else:
        print("Product has not been activated")
        logger.info("Product not activated")


def add_new_product_to_db(product: Scraper) -> None:
    product_to_db = Format.scraper_to_db_product(product, True)
    db.add(product_to_db)


def add_new_datapoint_to_db(product_code: str, price: float, currency: str, date: str | None = None):
    """Parameter 'date' defaults to the date of today in the format: YYYY-MM-DD"""
    if date is None:
        date = datetime.today().strftime("%Y-%m-%d")

    new_datapoint = db.DataPoint(
        product_code=product_code,
        date=date,
        price=price,
        currency=currency,
    )

    db.add(new_datapoint)


def add_new_datapoint_with_scraper(product: Scraper, date: str | None = None) -> None:
    if not product.product_info or not product.product_info.valid:
        print(f"Product info is not valid - category: '{product.category}' - url: {product.url}")
        return

    product_code = product.product_info.id
    price = product.product_info.price
    currency = product.product_info.currency

    add_new_datapoint_to_db(product_code, price, currency, date)


def update_products_is_active_with_product_codes(product_codes: list[str], is_active: bool) -> None:
    action = "Activating" if is_active else "Deactivating"

    for product_code in product_codes:
        print(f"{action} {product_code}")
        product = db.get_product_by_product_code(product_code)
        set_existing_product_is_active(product, is_active)


def set_existing_product_is_active(product: db.Product, is_active: bool) -> None:
    product.is_active = is_active
    db.add(product)


def is_missing_url_schema(url: str) -> bool:
    return not any(schema in url for schema in URL_SCHEMES)
