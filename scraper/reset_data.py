from typing import List
import logging

from scraper import Filemanager


def reset(categories: List[str], names: List[str], ids: List[str], all: bool) -> None:
    print("Resetting data...")

    record_data = Filemanager.get_record_data()

    if all:
        logging.getLogger(__name__).info("Resetting all products")
        reset_all(record_data)
        return

    logging.getLogger(__name__).info(f"Resetting categories: {categories}, product names: {names} and product ids: {ids}")

    for category_name, category_dict in record_data.items():
        if category_name in categories:
            reset_category(category_dict)
            continue

        for product_name, product_dict in category_dict.items():
            if product_name in names:
                reset_product(product_dict)
                continue

            for website_dict in product_dict.values():
                if str(website_dict["info"]["id"]) in ids:
                    reset_product_website(website_dict)

    Filemanager.save_record_data(record_data)


def reset_all(record_data: dict) -> None:
    for category_dict in record_data.values():
        reset_category(category_dict)

    Filemanager.save_record_data(record_data)


def reset_category(category_dict: dict) -> None:
    for product_dict in category_dict.values():
        reset_product(product_dict)


def reset_product(product_dict: dict) -> None:
    for website_dict in product_dict.values():
        reset_product_website(website_dict)


def reset_product_website(website_dict: dict) -> None:
    website_dict["info"] = {"id": "", "url": "", "currency": ""}
    website_dict["datapoints"] = []


def hard_reset():
    print("Hard resetting data...")
    logging.getLogger(__name__).info("Hard resetting data")

    data = {}
    Filemanager.save_record_data(data)
    Filemanager.clear_product_csv()
