from typing import List, Tuple
import logging
import pandas as pd

from scraper.filemanager import Filemanager


def delete(categories: List[str], names: List[str], ids: List[str], all: bool) -> None:
    print("Deleting...")
    record_data = Filemanager.get_record_data()

    if all:
        print("Deleting all products and categories...")
        logging.getLogger(__name__).info("Deleting all products and categories")
        delete_all()
        return

    logging.getLogger(__name__).info(f"Deleting categories: {categories}, product names: {names} and product ids: {ids}")
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

    categories_to_delete, products_to_delete_names, products_to_delete_ids = get_categories_products_ids_to_delete(
        record_data, category_names_to_delete, names_to_delete, ids_to_delete
    )

    products_df = Filemanager.get_products_data()

    # Delete product ids
    for product_to_delete_id in products_to_delete_ids:
        category_name, product_name, website_name = product_to_delete_id
        deleted_website_dict = record_data[category_name][product_name].pop(website_name)
        url_to_delete = deleted_website_dict["info"]["url"]

        # Delete row in products_df that match with the products that are deleted from record_data
        products_df = delete_dataframe_rows(products_df, "short_url", url_to_delete)

    # Delete product names
    for product_to_delete_name in products_to_delete_names:
        category_name, product_name = product_to_delete_name
        deleted_product_dict = record_data[category_name].pop(product_name)

        # Delete row in products_df that match with the products that are deleted from record_data
        for deleted_website_dict in deleted_product_dict.values():
            url_to_delete = deleted_website_dict["info"]["url"]
            products_df = delete_dataframe_rows(products_df, "short_url", url_to_delete)

    # Delete categories
    for category_to_delete in categories_to_delete:
        deleted_category_dict = record_data.pop(category_to_delete)

        # Delete row in products_df that match with the products that are deleted from record_data
        for deleted_product_dict in deleted_category_dict.values():
            for deleted_website_dict in deleted_product_dict.values():
                url_to_delete = deleted_website_dict["info"]["url"]
                products_df = delete_dataframe_rows(products_df, "short_url", url_to_delete)

    Filemanager.save_products_data(products_df)


def get_categories_products_ids_to_delete(
    record_data, category_names_to_delete, names_to_delete, ids_to_delete
) -> Tuple[List[str], List[Tuple[str, str]], List[Tuple[str, str, str]]]:
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

    return categories_to_delete, products_to_delete_names, products_to_delete_ids


def delete_dataframe_rows(products_df: pd.DataFrame, df_search_column: str, delete_value: str) -> pd.DataFrame:
    # get the indexes to keep (not delete)
    indexes_to_keep = products_df.index[products_df[df_search_column] != delete_value].tolist()
    # get new dataframe with only the indexes to keep
    new_products_df = products_df.loc[indexes_to_keep]
    return new_products_df
