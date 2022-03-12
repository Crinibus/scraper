from typing import List
from .filemanager import Filemanager


def search(queries: List[str]):
    print("Searching...")

    for query in queries:
        search_functions = [search_product_name, search_categories]
        searching_for_names = [
            ("product names", "product name(s)"),
            ("categories", "categories"),
        ]

        for search_function, searching_for_name in zip(search_functions, searching_for_names):
            results = search_function(query)

            if not results:
                print(f"\nFound nothing for search term '{query}' when searching for {searching_for_name[0]}")
                continue

            print(f"\nFound these {searching_for_name[1]} with search term '{query}':")
            for result in results:
                print(f"> {result}")
        print()


def search_product_name(product_name_search: str):
    records_data = Filemanager.get_record_data()

    matched_product_names = []

    for category_info in records_data.values():
        for product_name in category_info.keys():
            if product_name_search.lower() in product_name.lower():
                matched_product_names.append(product_name)
    return matched_product_names


def search_categories(category_search: str):
    records_data = Filemanager.get_record_data()

    matched_categories = []

    for category_name in records_data.keys():
        if category_search.lower() in category_name.lower():
            matched_categories.append(category_name)
    return matched_categories
