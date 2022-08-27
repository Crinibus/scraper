from typing import List
from .filemanager import Filemanager


def search(queries: List[str]):
    print("Searching...")

    records_data = Filemanager.get_record_data()

    for query in queries:
        search_functions = [search_product_name, search_categories]
        searching_for_names = [
            ("product names", "product name(s)"),
            ("categories", "categories"),
        ]

        for search_function, searching_for_name in zip(search_functions, searching_for_names):
            results = search_function(query, records_data)

            if not results:
                print(f"\nFound nothing for search term '{query}' when searching for {searching_for_name[0]}")
                continue

            print(f"\nFound these {searching_for_name[1]} with search term '{query}':")
            for result in results:
                print(f"> {result}")
        print()


def search_product_name(product_name_search: str, records_data: dict) -> List[str]:
    matched_products = []

    for category_dict in records_data.values():
        for product_name, product_dict in category_dict.items():
            if product_name_search.lower() in product_name.lower():
                for website_name, website_dict in product_dict.items():
                    id = website_dict["info"]["id"]
                    matched_products.append(f"{product_name} - {website_name.capitalize()} - {id}")
    return matched_products


def search_categories(category_search: str, records_data: dict) -> List[str]:
    matched_categories = []

    for category_name in records_data.keys():
        if category_search.lower() in category_name.lower():
            matched_categories.append(category_name)
    return matched_categories
