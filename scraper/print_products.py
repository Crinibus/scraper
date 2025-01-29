from scraper.constants import CHECK_MARK
import scraper.database as db
from scraper.database.models import Product
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
    if not products:
        print("Found no products")
        return

    grouped_products = db.group_products_by_names(products)

    for products in grouped_products:
        product_infos = db.get_product_infos_from_products(products)
        print(product_infos[0].product_name)

        for product_info in product_infos:
            print_latest_datapoint(product_info)
        print()


def print_latest_datapoint(product_info: ProductInfo) -> None:
    if not product_info.datapoints:
        print(f"> No datapoints for {product_info.id}")
        return

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

    if not categories:
        print("No products")
        return

    for category in categories:
        print(category)

        products = db.get_products_by_categories([category])

        grouped_products = db.group_products_by_names(products)

        list_grouped_products(grouped_products)


def list_products_with_filters(names: list[str] | None, product_codes: list[str] | None, categories: list[str] | None) -> None:
    print("\n----- LISTING PRODUCTS -----")
    products_by_filters: list[Product] = []

    if names:
        products_with_names = db.get_products_by_names(names)
        products_by_filters.extend(products_with_names)

    if product_codes:
        products_with_product_codes = db.get_products_by_product_codes(product_codes)
        products_by_filters.extend(products_with_product_codes)

    if categories:
        products_with_categories = db.get_products_by_categories(categories)
        products_by_filters.extend(products_with_categories)

    if not products_by_filters:
        print("Found no products with filters")
        return

    categories = set([product.category for product in products_by_filters])
    sorted_categories = sorted(categories)

    for category in sorted_categories:
        print(category)

        products_with_category = [product for product in products_by_filters if product.category == category]

        grouped_products = db.group_products_by_names(products_with_category)

        list_grouped_products(grouped_products)


def list_grouped_products(grouped_products: list[list[Product]]) -> None:
    for products in grouped_products:
        print(f"  > {products[0].name}")
        for product in products:
            is_active_marker = f"{CHECK_MARK} " if product.is_active else ""
            print(f"    - {is_active_marker}{product.domain.upper()} - {product.product_code}")
    print()
