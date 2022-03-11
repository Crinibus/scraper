from typing import List
from .filemanager import Filemanager


def search(queries: List[str]):
    print("Searching...")

    for product_name in queries:
        search_functions = [search_product_name, search_categories]
        searching_for_names = [
            ("product names", "product name(s)"),
            ("categories", "categories"),
        ]

        for search_function, searching_for_name in zip(search_functions, searching_for_names):
            results = search_function(product_name)

            if not results:
                print(f"\nFound nothing for search term '{product_name}' when searching for {searching_for_name[0]}")
                continue

            print(f"\nFound these {searching_for_name[1]} with search term '{product_name}':")
            for result in results:
                print(f"> {result}")
        print()

    # for product_name in queries:
    #     results = search_product_name(product_name)

    #     if not results:
    #         print(f"\nFound nothing for search term '{product_name}' when searching for product names")
    #         continue

    #     print(f"\nFound these product names with search term '{product_name}':")
    #     for result in results:
    #         print(f"> {result}")

    # for category in queries:
    #     results = search_categories(category)

    #     if not results:
    #         print(f"\nFound nothing for search term '{category}' when searching for category names")
    #         continue

    #     print(f"\nFound these product names with search term '{category}':")
    #     for result in results:
    #         print(f"> {result}")


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
