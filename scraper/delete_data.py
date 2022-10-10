from typing import List, Tuple

from scraper.filemanager import Filemanager


def delete(categories: List[str], names: List[str], ids: List[str], all: bool) -> None:
    record_data = Filemanager.get_record_data()

    if all:
        delete_all()
        return

    delete_from_record_data(record_data, categories, names, ids)

    Filemanager.save_record_data(record_data)


def delete_all() -> None:
    # Save an empty dictionary
    Filemanager.save_record_data({})


def delete_from_record_data(
    record_data: dict,
    category_names_to_delete: List[str] = None,
    names_to_delete: List[str] = None,
    ids_to_delete: List[str] = None,
) -> None:
    category_names_to_delete = [] if category_names_to_delete is None else category_names_to_delete
    names_to_delete = [] if names_to_delete is None else names_to_delete
    ids_to_delete = [] if ids_to_delete is None else ids_to_delete

    categories_to_delete: List[str] = []
    products_to_delete_names: List[Tuple[str, str]] = []
    products_to_delete_ids: List[Tuple[str, str, str]] = []

    # Find the "paths" for categories, product names and ids to delete
    for category_name, category_dict in record_data.items():
        if category_name in category_names_to_delete:
            categories_to_delete.append(category_name)

        for product_name, product_dict in category_dict.items():
            if product_name in names_to_delete:
                products_to_delete_names.append((category_name, product_name))

            for website_name, website_dict in product_dict.items():
                if website_dict["info"]["id"] in ids_to_delete:
                    products_to_delete_ids.append((category_name, product_name, website_name))

    # Delete product ids
    for product_to_delete_id in products_to_delete_ids:
        category_name, product_name, website_name = product_to_delete_id
        record_data[category_name][product_name].pop(website_name)

    # Delete product names
    for product_to_delete_name in products_to_delete_names:
        category_name, product_name = product_to_delete_name
        record_data[category_name].pop(product_name)

    # Delete categories
    for category_to_delete in categories_to_delete:
        record_data.pop(category_to_delete)
