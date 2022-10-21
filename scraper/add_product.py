from typing import List
import logging
from scraper.exceptions import WebsiteNotSupported
from scraper.scrape import Scraper
from scraper.filemanager import Filemanager
from scraper.domains import get_website_name, SUPPORTED_DOMAINS


def add_products(categories: List[str], urls: List[str]):
    for category, url in zip(categories, urls):
        try:
            add_product(category, url)
        except WebsiteNotSupported as err:
            logging.getLogger(__name__).error(err)
            print(err)


def add_product(category: str, url: str) -> None:
    logger = logging.getLogger(__name__)

    website_name = get_website_name(url)

    if website_name not in SUPPORTED_DOMAINS:
        raise WebsiteNotSupported(website_name)

    print(f"Adding product with category '{category}' and url '{url[0:min(50, len(url))]}'...")
    logger.info(f"Adding product with category '{category}' and url '{url}'")

    new_product = Scraper(category, url)
    new_product.scrape_info()

    if not check_if_product_exists(new_product):
        save_product(new_product)
        return

    user_input = input(
        "A product with the same name and from the same website already exist in your data, "
        "do you want to override this product? (y/n) > "
    )

    if user_input.lower() in ("y", "yes"):
        print("Overriding product...")
        save_product(new_product)
    else:
        print("Product was not added nor overrided")
        logger.info("Adding product cancelled")


def check_if_product_exists(product: Scraper) -> bool:
    data = Filemanager.get_record_data()

    category = product.category
    product_name = product.product_info.name
    website_name = product.website_handler.website_name

    try:
        data[category][product_name][website_name]
    except KeyError:
        return False

    return True


def save_product(product: Scraper):
    add_product_to_records(product)

    if not check_if_product_exists_csv(product):
        Filemanager.add_product_to_csv(product.category, product.url, product.website_handler.get_short_url())

    product.save_info()


def add_product_to_records(product: Scraper) -> None:
    data = Filemanager.get_record_data()

    category = product.category
    product_name = product.product_info.name
    website_name = product.website_handler.website_name

    empty_product_dict = {website_name: {"info": {}, "datapoints": []}}

    if not data.get(category):
        data.update({category: {product_name: empty_product_dict}})

    if data[category].get(product_name):
        data[category][product_name].update(empty_product_dict)
    else:
        data[category].update({product_name: empty_product_dict})

    Filemanager.save_record_data(data)


def check_if_product_exists_csv(product: Scraper):
    products_df = Filemanager.get_products_data()

    for category, url in zip(products_df["category"], products_df["url"]):
        if product.category.lower() == category.lower() and product.url == url:
            return True

    return False
