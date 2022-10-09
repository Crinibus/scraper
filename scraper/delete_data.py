from typing import List, Tuple

from scraper.filemanager import Filemanager


def delete(categories: List[str], names: List[str], ids: List[str], all: bool) -> None:
    record_data = Filemanager.get_record_data()

    if all:
        delete_all()
        return

    if ids:
        delete_product_ids(ids, record_data)

    if names:
        delete_product_names(names, record_data)

    if categories:
        delete_categories(categories, record_data)


def delete_all() -> None:
    # Save an empty dictionary
    Filemanager.save_record_data({})


def delete_product_ids(ids: List[str], record_data: dict) -> None:
    products_to_delete: List[Tuple[str, str, str]] = []

    for category_name, category_dict in record_data.items():
        for product_name, product_dict in category_dict.items():
            for website_name, website_dict in product_dict.items():
                if website_dict["info"]["id"] in ids:
                    products_to_delete.append((category_name, product_name, website_name))

    for product_to_delete in products_to_delete:
        category_name, product_name, website_name = product_to_delete
        record_data[category_name][product_name].pop(website_name)

    Filemanager.save_record_data(record_data)


def delete_product_names(names: List[str], record_data: dict) -> None:
    pass


def delete_categories(categories: List[str], record_data: dict) -> None:
    pass
