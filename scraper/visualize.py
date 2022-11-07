from typing import Iterator, List
import plotly.graph_objs as go
from scraper.filemanager import Filemanager
from scraper.constants import WEBSITE_COLORS
from datetime import datetime


def visualize_data(
    show_all: bool, categories: List[str], ids: List[str], names: List[str], only_up_to_date: bool, compare: bool
) -> None:
    print("Visualizing...")

    if compare:
        compare_products(ids, names)
        return

    if show_all:
        show_all_products(only_up_to_date)

    if categories:
        for category in categories:
            show_category(category, only_up_to_date)

    if ids:
        for id in ids:
            show_id(id)

    if names:
        for name in names:
            show_name(name)


def show_id(id: str) -> None:
    product_data = get_product_with_id(id)

    if not product_data:
        print(f"Couldn't find product with id: {id}")
        return

    print(f"Visualizing product with id: {id}")

    product_name = product_data["name"]
    product_info = product_data["info"]

    fig = go.Figure()
    add_scatter_plot(
        fig,
        product_info["website_name"],
        str(product_info["id"]),
        product_info["currency"],
        product_info["dates"],
        product_info["prices"],
    )

    title = f"Price(s) of {product_name.upper()} - ID {product_info['id']}"

    title_with_status = append_status_to_title(title, product_info["dates"])

    config_figure(fig, title_with_status)
    fig.show()


def show_category(category: str, only_up_to_date: bool) -> None:
    print(f"Visualizing products in category: {category.lower()}")

    for product_info in get_products_with_category(category):
        product_name = product_info["name"]
        fig = go.Figure()

        is_up_to_date = False

        for website_info in product_info["websites"]:
            add_scatter_plot(
                fig,
                website_info["website_name"],
                str(website_info["id"]),
                website_info["currency"],
                website_info["dates"],
                website_info["prices"],
            )

            if check_if_dates_up_to_date(website_info["dates"]):
                is_up_to_date = True

        if only_up_to_date and not is_up_to_date:
            continue

        title = f"Price(s) of {product_name.upper()}"

        title_with_status = append_status_to_title_bool(title, is_up_to_date)

        config_figure(fig, title_with_status)
        fig.show()


def show_name(name: str) -> None:
    product_info = get_product_with_name(name)

    if not product_info:
        print(f"Couldn't find product with name: {name.lower()}")
        return

    print(f"Visualizing product with name: {name.lower()}")

    fig = go.Figure()

    is_up_to_date = False

    for website_info in product_info["websites"]:
        add_scatter_plot(
            fig,
            website_info["website_name"],
            str(website_info["id"]),
            website_info["currency"],
            website_info["dates"],
            website_info["prices"],
        )

        if check_if_dates_up_to_date(website_info["dates"]):
            is_up_to_date = True

    title = f"Price(s) of {name.upper()}"

    title_with_status = append_status_to_title_bool(title, is_up_to_date)

    config_figure(fig, title_with_status)
    fig.show()


def show_all_products(only_up_to_date: bool) -> None:
    if only_up_to_date:
        print("Visualizing all products that are up to date...")
    else:
        print("Visualizing all products...")

    for product_info in get_all_products():
        fig = go.Figure()

        is_up_to_date = False

        for website_info in product_info["websites"]:
            add_scatter_plot(
                fig,
                website_info["website_name"],
                str(website_info["id"]),
                website_info["currency"],
                website_info["dates"],
                website_info["prices"],
            )

            if check_if_dates_up_to_date(website_info["dates"]):
                is_up_to_date = True

        if only_up_to_date and not is_up_to_date:
            continue

        title = f"Price(s) of {product_info['name'].upper()}"

        title_with_status = append_status_to_title_bool(title, is_up_to_date)

        config_figure(fig, title_with_status)
        fig.show()


def compare_products(ids: List[str], names: List[str]) -> None:
    products_with_ids = get_products_with_ids(ids)
    products_with_name = get_products_with_names(names)

    products = [*products_with_ids, *products_with_name]

    if len(products_with_ids) < len(ids) or len(products_with_name) < len(names):
        print("\nCouldn't find all products that have the specified id(s) or name(s), only comparing those that are found\n")

    product_ids = [product["info"]["id"] for product in products]
    product_ids_string = ", ".join(product_ids)

    print(f"Comparing products with ids: {product_ids_string}")

    fig = go.Figure()

    for product in products:
        product_name = product["name"]
        product_info = product["info"]
        product_id = product_info["id"]

        add_scatter_plot(
            fig,
            product_info["website_name"],
            str(product_id),
            product_info["currency"],
            product_info["dates"],
            product_info["prices"],
            name=f"{product_id} - {product_name}",
        )

    title = f"Comparing products with ids {product_ids_string}"

    config_figure(fig, title)
    fig.show()


def format_data() -> Iterator[dict]:
    records_data = Filemanager.get_record_data()

    for category_name, category_info in records_data.items():
        for product_name, product_info in category_info.items():
            product_data = {
                "name": product_name,
                "category": category_name,
                "websites": [],
            }

            for website_name, website_info in product_info.items():
                dates: List[str] = [datapoint["date"] for datapoint in website_info["datapoints"]]
                prices: List[float] = [datapoint["price"] for datapoint in website_info["datapoints"]]

                product_data["websites"].append(
                    {
                        "website_name": website_name,
                        "id": website_info["info"]["id"],
                        "currency": website_info["info"]["currency"],
                        "dates": dates,
                        "prices": prices,
                    }
                )

            yield product_data


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
    dates: List[str],
    prices: List[float],
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


def get_products_with_category(category_name: str) -> Iterator[dict]:
    for product_info in format_data():
        if product_info["category"].lower() == category_name.lower():
            yield product_info


def get_product_with_id(id: str) -> dict:
    for product_info in format_data():
        for website_info in product_info["websites"]:
            if id == str(website_info["id"]):
                return {
                    "name": product_info["name"],
                    "category": product_info["category"],
                    "info": website_info,
                }
    return None


def get_products_with_ids(ids: List[str]) -> List[dict]:
    products = []
    for product_info in format_data():
        for website_info in product_info["websites"]:
            if str(website_info["id"]) in ids:
                products.append(
                    {
                        "name": product_info["name"],
                        "category": product_info["category"],
                        "info": website_info,
                    }
                )
    return products


def get_product_with_name(name: str) -> dict:
    for product_info in format_data():
        if product_info["name"].lower() == name.lower():
            return product_info
    return None


def get_products_with_names(names: List[str]) -> List[dict]:
    names_lowercase = [name.lower() for name in names]
    products = []
    for product_info in format_data():
        if not product_info["name"].lower() in names_lowercase:
            continue

        for website_info in product_info["websites"]:
            products.append(
                {
                    "name": product_info["name"],
                    "category": product_info["category"],
                    "info": website_info,
                }
            )
    return products


def get_all_products() -> Iterator[dict]:
    for product_info in format_data():
        yield product_info


def check_if_dates_up_to_date(dates: List[str]) -> bool:
    """check if today and the last date in dates is at most 1 day apart"""
    if len(dates) == 0:
        return False

    return is_date_up_to_date(dates[-1])


def is_date_up_to_date(date: str) -> bool:
    """check if today and date is at most 1 day apart"""
    latest_date = datetime.strptime(date, "%Y-%m-%d")
    date_diff = datetime.today() - latest_date

    return date_diff.days <= 1


def append_status_to_title(title: str, dates: list) -> str:
    if len(dates) == 0:
        return f"{title} - NO DATAPOINTS"

    is_up_to_date = is_date_up_to_date(dates[-1])

    return append_status_to_title_bool(title, is_up_to_date)


def append_status_to_title_bool(title: str, up_to_date: bool) -> str:
    if up_to_date:
        return f"{title} - UP TO DATE"

    return f"{title} - OUTDATED"
