import scraper.database as db


def search(search_terms: list[str]) -> None:
    print("Searching...")

    product_name_search_results = search_product_names(search_terms)
    categories_search_results = search_categories(search_terms)

    if product_name_search_results:
        print("\n--- Results from product name search ---")
        for result in product_name_search_results:
            print(f"> {result}\n")
    else:
        print("\nNo results for product name search")

    if categories_search_results:
        print("\n--- Results from category search ---")
        for result in categories_search_results:
            print(f"> {result}")
    else:
        print("\nNo results for categories search")


def search_product_names(search_terms: list[str]) -> list[str]:
    products_strings = []
    products = db.get_products_by_names_fuzzy(search_terms)

    if not products:
        return []

    grouped_products = db.group_products_by_names(products)

    for products in grouped_products:
        matched_domains = []
        for product in products:
            match_string = f" - {product.domain.capitalize()} - {product.product_code}"
            matched_domains.append(match_string)
        matched_domains_string = "\n".join(matched_domains)
        products_strings.append(f"{products[0].name}\n{matched_domains_string}")

    return products_strings


def search_categories(search_terms: list[str]) -> list[str]:
    all_results = []
    all_categories = db.get_all_unique_categories()

    for search_term in search_terms:
        results = [category for category in all_categories if search_term.lower() in category.lower()]
        all_results.extend(results)

    return all_results
