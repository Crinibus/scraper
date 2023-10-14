import scraper.database as db
from scraper.models.product import ProductInfo


def print_latest_datapoints(names: list[str], product_codes: list[str], categories: list[str]) -> None:
    if names:
        print("\n----- SHOWING LATEST DATAPOINT FOR NAME(s) -----")
        products = db.get_products_by_names(names)
        print_latest_datapoints_for_products(products)

    if product_codes:
        print("\n----- SHOWING LATEST DATAPOINT FOR ID(s) -----")
        products = db.get_products_by_product_codes(product_codes)
        print_latest_datapoints_for_products(products)

    if categories:
        print("\n----- SHOWING LATEST DATAPOINT FOR CATEGORY(s) -----")
        products = db.get_products_by_categories(categories)
        print_latest_datapoints_for_products(products)


def print_latest_datapoints_for_products(products: list[db.Product]):
    grouped_products = db.group_products_by_names(products)

    for products in grouped_products:
        product_infos = db.get_product_infos_from_products(products)
        print(product_infos[0].product_name.upper())

        for product_info in product_infos:
            print_latest_datapoint(product_info)
        print()


def print_latest_datapoint(product_info: ProductInfo) -> None:
    id = product_info.id
    website_name = product_info.website.capitalize()
    currency = product_info.currency
    latest_datapoint = product_info.datapoints[-1]
    date = latest_datapoint.date
    price = latest_datapoint.price
    print(f"> {website_name} - {id}\n  - {currency} {price}\n  - {date}")


def print_all_products() -> None:
    print("\n----- SHOWING ALL PRODUCTS -----")
    categories = db.get_all_unique_categories()

    for category in categories:
        print(category.upper())

        products = db.get_products_by_categories([category])

        grouped_products = db.group_products_by_names(products)

        for products in grouped_products:
            print(f"  > {products[0].name.upper()}")
            for product in products:
                is_active_marker = "\u2713 " if product.is_active else ""
                print(f"    - {is_active_marker}{product.domain.upper()} - {product.product_code}")
        print()
