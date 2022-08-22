from typing import List
import logging
from scraper.scrape import Scraper
from scraper.filemanager import Filemanager
from scraper.domains import get_website_name, VALID_DOMAINS


def add_products(categories: List[str], urls: List[str]):
    for category, url in zip(categories, urls):
        add_product(category, url)


def add_product(category: str, url: str) -> None:
    print("Adding product...")
    logger = logging.getLogger(__name__)
    logger.info(f"Adding product: {category} - {url}")

    website_name = get_website_name(url)

    if website_name not in VALID_DOMAINS:
        print(f"Can't scrape from this website: {website_name}")
        logger.info(f"Not supported website to scrape from: {website_name}")
        return

    new_product = Scraper(category, url)
    new_product.scrape_info()

    product_exists = check_if_product_exists(new_product)

    if not product_exists:
        add_product_to_records(new_product)
        if not check_if_product_exists_csv(new_product):
            Filemanager.add_product_to_csv(new_product.category, new_product.url)
        new_product.save_info()
        return

    user_input = input(
        "A product with the same name and from the same website already exist in your data, "
        "do you want to override this product? (y/n) > "
    )

    if user_input.lower() in ("y", "yes"):
        print("Overriding product...")
        add_product_to_records(new_product)

        if not check_if_product_exists_csv(new_product):
            Filemanager.add_product_to_csv(new_product.category, new_product.url)

        new_product.save_info()
    else:
        print("Product was not added nor overrided")
        logger.info("Adding product cancelled")


def check_if_product_exists(product: Scraper) -> bool:
    data = Filemanager.get_record_data()

    try:
        data[product.category][product.product_info.name][product.website_handler.website_name]
    except KeyError:
        return False

    return True


def add_product_to_records(product: Scraper) -> None:
    data = Filemanager.get_record_data()

    empty_product_dict = {product.website_handler.website_name: {"info": {}, "datapoints": []}}

    if not data.get(product.category):
        data.update({product.category: {product.product_info.name: empty_product_dict}})

    if data[product.category].get(product.product_info.name):
        data[product.category][product.product_info.name].update(empty_product_dict)
    else:
        data[product.category].update({product.product_info.name: empty_product_dict})

    Filemanager.save_record_data(data)


def check_if_product_exists_csv(product: Scraper):
    products_df = Filemanager.get_products_data()

    for category, url in zip(products_df["category"], products_df["url"]):
        if product.category.lower() == category.lower() and product.url == url:
            return True

    return False
