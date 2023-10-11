import scraper.database as db
from scraper.models.product import ProductInfo


def print_latest_datapoints(names: list[str], product_codes: list[str]) -> None:
    if names:
        print("\n----- SHOWING LATEST DATAPOINT FOR NAME(s) -----")
        products = db.get_products_by_names(names)
        print_latest_datapoints_for_products(products)

    if product_codes:
        print("\n----- SHOWING LATEST DATAPOINT FOR ID(s) -----")
        products = db.get_products_by_product_codes(product_codes)
        print_latest_datapoints_for_products(products)


def print_latest_datapoints_for_products(products: list[db.Product]):
    product_infos = db.get_product_infos_from_products(products)

    for product_info in product_infos:
        print(product_info.product_name.upper())
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
                print(f"    - {product.domain.upper()} - {product.id}")
        print()
