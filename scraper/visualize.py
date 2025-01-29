from typing import Iterable, Iterator
import plotly.graph_objs as go
from datetime import datetime

import scraper.database as db
from scraper.models import DataPointInfo, ProductInfo, MasterProduct
from scraper.constants import WEBSITE_COLORS


def visualize_data(
    show_all: bool, categories: list[str], ids: list[str], names: list[str], only_up_to_date: bool, compare: bool
) -> None:
    print("Visualizing...")

    # Convert all string to lowercase
    categories = [category.lower() for category in categories]
    ids = [id.lower() for id in ids]
    names = [name.lower() for name in names]

    master_products = get_master_products()

    if not master_products:
        print("No products saved")
        return

    if compare:
        compare_products(master_products, ids, names, categories, only_up_to_date, show_all)
        return

    if show_all:
        show_master_products(master_products, only_up_to_date)

    if categories:
        for master_product in get_master_products_with_categories(master_products, categories, only_up_to_date):
            product_name = master_product.product_name
            category = master_product.category
            status_of_master_product = get_status_of_master_product(master_product)
            title = f"Price(s) of {product_name} - {category} - {status_of_master_product}"
            show_products(master_product.products, title)
        else:
            print("No products found with category/categories")

    if ids:
        for product in get_products_with_ids(master_products, ids, only_up_to_date):
            status_of_product = get_status_of_product(product)
            product_name = product.product_name
            title = f"Price(s) of {product_name} - {status_of_product}"
            show_product(product, title)
        else:
            print("No products found with id(s)")

    if names:
        for master_product in get_master_products_with_names(master_products, names, only_up_to_date):
            product_name = master_product.product_name
            status_of_master_product = get_status_of_master_product(master_product)
            title = f"Price(s) of {product_name} - {status_of_master_product}"
            show_products(master_product.products, title)
        else:
            print("No products found with name(s)")


def compare_products(
    master_products: tuple[MasterProduct],
    ids: list[str],
    names: list[str],
    categories: list[str],
    only_up_to_date: bool,
    show_all: bool,
) -> None:
    master_products_with_names = get_master_products_with_names(master_products, names, only_up_to_date)
    products_with_names = get_products_from_master_products(master_products_with_names)

    products_with_ids = list(get_products_with_ids(master_products, ids, only_up_to_date))

    master_products_with_categories = get_master_products_with_categories(master_products, categories, only_up_to_date)
    products_with_categories = get_products_from_master_products(master_products_with_categories)

    products_to_compare = [*products_with_ids, *products_with_names, *products_with_categories]

    if show_all:
        products_to_compare = get_products_from_master_products(master_products)

    if not products_to_compare:
        print("No products found to compare")
        return

    product_ids = [product.id for product in products_to_compare]
    product_ids_string = ", ".join(product_ids)
    title_ = product_ids_string[:100] + " ..." if len(product_ids_string) > 100 else product_ids_string
    show_products(products_to_compare, f"Comparing products with ids: {title_}")


def show_master_products(master_products: tuple[MasterProduct], only_up_to_date: bool) -> None:
    if not master_products:
        print("No products found")
        return

    for master_product in master_products:
        if only_up_to_date and not is_master_product_up_to_date(master_product):
            continue

        status_of_master_product = get_status_of_master_product(master_product)
        show_products(master_product.products, f"Price(s) of {master_product.product_name} - {status_of_master_product}")


def show_product(product: ProductInfo, title: str) -> None:
    show_products([product], title)


def show_products(products: list[ProductInfo], title: str) -> None:
    fig = go.Figure()
    for product in products:
        add_scatter_plot(
            fig,
            product,
            name_format="%website - %name - %id",
        )

    num_products = len(products)

    config_figure(fig, title, num_products)
    fig.show(config={"scrollZoom": True})


def get_master_products() -> tuple[MasterProduct]:
    master_products: list[MasterProduct] = []

    all_products = db.get_all_products_with_datapoints()

    unique_product_names = set([product.product_name for product in all_products])

    for unique_product_name in unique_product_names:
        products_from_db = db.get_products_by_names([unique_product_name])
        products = db.get_product_infos_from_products(products_from_db)

        category = products[0].category
        master_product = MasterProduct(unique_product_name, category, products)
        master_products.append(master_product)

    return tuple(master_products)


def get_products_with_ids(
    master_products: tuple[MasterProduct], ids: list[str], only_up_to_date: bool
) -> Iterator[ProductInfo]:
    for master_product in master_products:
        for product in master_product.products:
            if only_up_to_date and not product.is_up_to_date:
                continue

            if product.id.lower() not in ids:
                continue

            yield product


def get_master_products_with_categories(
    master_products: tuple[MasterProduct], categories: list[str], only_up_to_date: bool
) -> Iterator[MasterProduct]:
    for master_product in master_products:
        if master_product.category.lower() not in categories:
            continue

        if only_up_to_date and not is_master_product_up_to_date(master_product):
            continue

        yield master_product


def get_master_products_with_names(
    master_products: tuple[MasterProduct], names: list[str], only_up_to_date: bool
) -> Iterator[MasterProduct]:
    for master_product in master_products:
        if master_product.product_name.lower() not in names:
            continue

        if only_up_to_date and not is_master_product_up_to_date(master_product):
            continue

        yield master_product


def get_products_from_master_products(master_products: Iterable[MasterProduct]) -> list[ProductInfo]:
    return [product for master_product in master_products for product in master_product.products]


def get_yvalue_for_configure_figure(num_products: int, min_value: int, max_value: int, max_num: int):
    value = ((num_products / max_num) * (max_value - min_value)) + min_value

    if value > max_value:
        value = max_value
    elif value < min_value:
        value = min_value

    return value


def config_figure(figure: go.Figure, figure_title: str, num_products: int) -> None:
    figure.update_traces(mode="markers+lines", hovertemplate=None)

    y_value = get_yvalue_for_configure_figure(num_products, 0.1, 0.25, 30)

    figure.update_layout(
        title=dict(text=figure_title),
        xaxis_title="Date",
        yaxis_title="Price",
        hovermode="closest",
        separators=".,",
        legend=dict(orientation="h", y=-y_value, x=0, yref="paper", xref="paper", yanchor="top", xanchor="left"),
        hoverlabel_namelength=-1,
    )


def add_scatter_plot(
    figure: go.Figure,
    product: ProductInfo,
    color: str = None,
    hover_text: str = None,
    name_format: str = None,
) -> None:
    scatter_name = product.to_string_format(name_format) if name_format else f"{product.website.capitalize()} - {product.id}"
    scatter_color = color if color else WEBSITE_COLORS[product.website]
    scatter_hover_text = hover_text if hover_text else "Price: %{y:.0f}" + f" {product.currency}"

    figure.add_trace(
        go.Scatter(
            name=scatter_name,
            x=product.get_all_dates(),
            y=product.get_all_prices(),
            line={"color": scatter_color, "width": 2},
            hovertemplate=scatter_hover_text,
        )
    )


def is_datapoints_up_to_date(datapoints: list[DataPointInfo]) -> bool:
    """check if today and the last date in datapoints is at most 1 day apart"""
    if len(datapoints) == 0:
        return False

    return is_date_up_to_date(datapoints[-1].date)


def is_date_up_to_date(date: str) -> bool:
    """check if today and date is at most 1 day apart"""
    latest_date = datetime.strptime(date, "%Y-%m-%d")
    date_diff = datetime.today() - latest_date

    return date_diff.days <= 1


def is_master_product_up_to_date(master_product: MasterProduct) -> bool:
    return any((product.is_up_to_date for product in master_product.products))


def get_status_of_master_product(master_product: MasterProduct) -> str:
    if is_master_product_up_to_date(master_product):
        return get_status_of_product_by_bool(True)

    return get_status_of_product_by_bool(False)


def get_status_of_product(product: ProductInfo) -> str:
    return get_status_of_product_by_bool(product.is_up_to_date)


def get_status_of_product_by_bool(up_to_date: bool) -> str:
    return "UP TO DATE" if up_to_date else "OUTDATED"
