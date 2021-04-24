from typing import Generator
import plotly.graph_objs as go
from scraper.filemanager import Filemanager
from scraper.constants import WEBSITE_COLORS


def show_id(id: str) -> None:
    print(f"Visualizing product with id: {id}")

    product_data = get_product_with_id(id)

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

    config_figure(fig, f"Price(s) of {product_name.upper()} - ID {product_info['id']}")
    fig.show()


def show_category(category: str) -> None:
    print(f"Visualizing products in category: {category.lower()}")

    for product_info in get_products_with_category(category):
        product_name = product_info["name"]
        fig = go.Figure()

        for website_info in product_info["websites"]:
            add_scatter_plot(
                fig,
                website_info["website_name"],
                str(website_info["id"]),
                website_info["currency"],
                website_info["dates"],
                website_info["prices"],
            )

        config_figure(fig, f"Price(s) of {product_name.upper()}")
        fig.show()


def show_name(name: str) -> None:
    print(f"Visualizing product with name: {name.lower()}")

    product_info = get_product_with_name(name)

    fig = go.Figure()
    for website_info in product_info["websites"]:
        add_scatter_plot(
            fig,
            website_info["website_name"],
            str(website_info["id"]),
            website_info["currency"],
            website_info["dates"],
            website_info["prices"],
        )

    config_figure(fig, f"Price(s) of {name.upper()}")
    fig.show()


def show_all_products() -> None:
    print("Visualizing all products")

    for product_info in get_all_products():
        fig = go.Figure()
        for website_info in product_info["websites"]:
            add_scatter_plot(
                fig,
                website_info["website_name"],
                str(website_info["id"]),
                website_info["currency"],
                website_info["dates"],
                website_info["prices"],
            )

        config_figure(fig, f"Price(s) of {product_info['name'].upper()}")
        fig.show()


def format_data() -> dict:
    records_data = Filemanager.get_record_data()

    data = {"products": []}

    for category_name, category_info in records_data.items():
        for product_name, product_info in category_info.items():
            product_data = {
                "name": product_name,
                "category": category_name,
                "websites": [],
            }

            for website_name, website_info in product_info.items():
                dates = [datapoint["date"] for datapoint in website_info["datapoints"]]
                prices = [datapoint["price"] for datapoint in website_info["datapoints"]]
                product_data["websites"].append(
                    {
                        "website_name": website_name,
                        "id": website_info["info"]["id"],
                        "currency": website_info["info"]["currency"],
                        "dates": dates,
                        "prices": prices,
                    }
                )

            data["products"].append(product_data)

    return data


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
    dates: list,
    prices: list,
) -> None:
    figure.add_trace(
        go.Scatter(
            name=f"{website_name.capitalize()} - {id}",
            x=dates,
            y=prices,
            line={"color": WEBSITE_COLORS[website_name], "width": 2},
            hovertemplate="Price: %{y:.0f}" + f" {currency}",
        )
    )


def get_products_with_category(category_name: str) -> Generator[dict, None, None]:
    data = format_data()

    for product_info in data["products"]:
        if product_info["category"].lower() == category_name.lower():
            yield product_info


def get_product_with_id(id: str) -> dict:
    data = format_data()

    for product_info in data["products"]:
        for website_info in product_info["websites"]:
            if id == str(website_info["id"]):
                return {
                    "name": product_info["name"],
                    "category": product_info["category"],
                    "info": website_info,
                }


def get_product_with_name(name: str) -> dict:
    data = format_data()

    for product_info in data["products"]:
        if product_info["name"].lower() == name.lower():
            return product_info


def get_all_products() -> Generator[dict, None, None]:
    data = format_data()

    for product_info in data["products"]:
        yield product_info
