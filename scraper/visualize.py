from dataclasses import dataclass, field
from typing import Iterator
import plotly.graph_objs as go
from datetime import datetime

from scraper import Filemanager
from scraper.constants import WEBSITE_COLORS


@dataclass
class Datapoint:
    date: str
    price: float


@dataclass
class Product:
    product_name: str
    category: str
    url: str
    id: str
    currency: str
    website: str
    datapoints: list[Datapoint]
    is_up_to_date: bool

    def get_all_dates(self) -> list[str]:
        return [datapoint.date for datapoint in self.datapoints]

    def get_all_prices(self) -> list[float]:
        return [datapoint.price for datapoint in self.datapoints]


@dataclass
class MasterProduct:
    product_name: str
    category: str
    products: list[Product] = field(default_factory=list)


def visualize_data(
    show_all: bool, categories: list[str], ids: list[str], names: list[str], only_up_to_date: bool, compare: bool
) -> None:
    print("Visualizing...")

    # Convert all string to lowercase
    categories = [category.lower() for category in categories]
    ids = [id.lower() for id in ids]
    names = [name.lower() for name in names]

    records_data = Filemanager.get_record_data()
    master_products = get_master_products(records_data)

    if compare:
        compare_products(master_products, ids, names)
        return

    if show_all:
        show_master_products(master_products, only_up_to_date)

    if categories:
        for master_product in get_master_products_with_categories(master_products, categories, only_up_to_date):
            product_name = master_product.product_name.upper()
            category = master_product.category.upper()
            status_of_master_product = get_status_of_master_product(master_product)
            title = f"Price(s) of {product_name} - {category} - {status_of_master_product}"
            show_products(master_product.products, title)

    if ids:
        for product in get_products_with_ids(master_products, ids, only_up_to_date):
            status_of_product = get_status_of_product(product)
            product_name = product.product_name.upper()
            title = f"Price(s) of {product_name} - {status_of_product}"
            show_product(product, title)

    if names:
        for master_product in get_master_products_with_names(master_products, names, only_up_to_date):
            product_name = master_product.product_name.upper()
            status_of_master_product = get_status_of_master_product(master_product)
            title = f"Price(s) of {product_name} - {status_of_master_product}"
            show_products(master_product.products, title)


def compare_products(master_products: tuple[MasterProduct], ids: list[str], names: list[str]) -> None:
    master_products_with_names = get_master_products_with_names(master_products, names, False)
    products_with_names = [product for master_product in master_products_with_names for product in master_product.products]

    products_with_ids = list(get_products_with_ids(master_products, ids, False))

    products_to_compare = [*products_with_ids, *products_with_names]

    product_ids = [product.id for product in products_to_compare]
    product_ids_string = ", ".join(product_ids)

    show_products(products_to_compare, f"Comparing products with ids: {product_ids_string}")


def show_master_products(master_products: tuple[MasterProduct], only_up_to_date: bool) -> None:
    for master_product in master_products:
        status_of_master_product = get_status_of_master_product(master_product)
        show_products(
            master_product.products, f"Price(s) of {master_product.product_name.upper()} - {status_of_master_product}"
        )


def show_product(product: Product, title: str) -> None:
    fig = go.Figure()
    add_scatter_plot(
        fig,
        product.website,
        product.id,
        product.currency,
        product.get_all_dates(),
        product.get_all_prices(),
    )
    config_figure(fig, title)
    fig.show()


def show_products(products: list[Product], title: str) -> None:
    fig = go.Figure()
    for product in products:
        add_scatter_plot(
            fig,
            product.website,
            product.id,
            product.currency,
            product.get_all_dates(),
            product.get_all_prices(),
        )
    config_figure(fig, title)
    fig.show()


def get_master_products(records_data: dict) -> tuple[MasterProduct]:
    master_products: list[MasterProduct] = []

    for category_name, category_info in records_data.items():
        for product_name, product_info in category_info.items():
            master_product = MasterProduct(product_name, category_name)
            for website_name, website_info in product_info.items():
                id = website_info["info"]["id"]
                url = website_info["info"]["url"]
                currency = website_info["info"]["currency"]
                datapoints = [Datapoint(datapoint["date"], datapoint["price"]) for datapoint in website_info["datapoints"]]
                is_up_to_date = is_datapoints_up_to_date(datapoints)
                product = Product(product_name, category_name, url, id, currency, website_name, datapoints, is_up_to_date)
                master_product.products.append(product)
            master_products.append(master_product)

    return tuple(master_products)


def get_products_with_ids(master_products: tuple[MasterProduct], ids: list[str], only_up_to_date: bool) -> Iterator[Product]:
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

        if only_up_to_date and not any((product.is_up_to_date for product in master_product.products)):
            continue

        yield master_product


def get_master_products_with_names(
    master_products: tuple[MasterProduct], names: list[str], only_up_to_date: bool
) -> list[MasterProduct]:
    for master_product in master_products:
        if master_product.product_name.lower() not in names:
            continue

        if only_up_to_date and not any((product.is_up_to_date for product in master_product.products)):
            continue

        yield master_product


def config_figure(figure: go.Figure, figure_title: str) -> None:
    figure.update_traces(mode="markers+lines")
    figure.update_layout(
        title=figure_title,
        xaxis_title="Date",
        yaxis_title="Price",
        hovermode="x",
        separators=".,",
    )


def add_scatter_plot(
    figure: go.Figure,
    website_name: str,
    id: str,
    currency: str,
    dates: list[str],
    prices: list[float],
    name: str = None,
    color: str = None,
    hover_text: str = None,
) -> None:
    scatter_name = name if name else f"{website_name.capitalize()} - {id}"
    scatter_color = color if color else WEBSITE_COLORS[website_name]
    scatter_hover_text = hover_text if hover_text else "Price: %{y:.0f}" + f" {currency}"

    figure.add_trace(
        go.Scatter(
            name=scatter_name,
            x=dates,
            y=prices,
            line={"color": scatter_color, "width": 2},
            hovertemplate=scatter_hover_text,
        )
    )


def is_datapoints_up_to_date(datapoints: list[Datapoint]) -> bool:
    """check if today and the last date in datapoints is at most 1 day apart"""
    if len(datapoints) == 0:
        return False

    return is_date_up_to_date(datapoints[-1].date)


def is_date_up_to_date(date: str) -> bool:
    """check if today and date is at most 1 day apart"""
    latest_date = datetime.strptime(date, "%Y-%m-%d")
    date_diff = datetime.today() - latest_date

    return date_diff.days <= 1


def get_status_of_master_product(master_product: MasterProduct) -> str:
    if any((product.is_up_to_date for product in master_product.products)):
        return get_status_of_product_by_bool(True)

    return get_status_of_product_by_bool(False)


def get_status_of_product(product: Product) -> str:
    return get_status_of_product_by_bool(product.is_up_to_date)


def get_status_of_product_by_bool(up_to_date: bool) -> str:
    return "UP TO DATE" if up_to_date else "OUTDATED"


def main_test():
    # TODO - DELETE THIS FUNCTION
    visualize_data(False, ["højtAler"], [], ["kIngSton a2000 m.2 nvme ssd - 1tb"], False, False)
