import plotly.graph_objs as go
from scraper.filemanager import Filemanager
from scraper.constants import WEBSITE_COLORS


def show_id(id: str) -> None:
    print(f"Visualizing product with id: {id}")
    data = format_data()

    for category_name, category_info in data.items():
        for product_name, product_info in category_info.items():
            for website_name, website_info in product_info.items():
                if id == str(website_info["id"]):
                    fig = go.Figure()
                    fig.add_trace(
                        go.Scatter(
                            name=website_name.capitalize(),
                            x=website_info["dates"],
                            y=website_info["prices"],
                            line={"color": WEBSITE_COLORS[website_name], "width": 2},
                            hovertemplate="Price: %{y:.0f}",
                        )
                    )

                    fig.update_traces(mode="markers+lines")
                    fig.update_layout(
                        title=f"Price(s) of {product_name.upper()}",
                        xaxis_title="Date",
                        yaxis_title="Price",
                        hovermode="x",
                        separators=".,",
                    )

                    fig.show()


def show_category(category: str) -> None:
    print(f"Visualizing products in category: {category}")
    data = format_data()

    for category_name, category_info in data.items():
        if category == category_name:
            for product_name, product_info in category_info.items():
                fig = go.Figure()
                for website_name, website_info in product_info.items():
                    fig.add_trace(
                        go.Scatter(
                            name=website_name.capitalize(),
                            x=website_info["dates"],
                            y=website_info["prices"],
                            line={"color": WEBSITE_COLORS[website_name], "width": 2},
                            hovertemplate="Price: %{y:.0f}",
                        )
                    )

                fig.update_traces(mode="markers+lines")
                fig.update_layout(
                    title=f"Price(s) of {product_name.upper()}",
                    xaxis_title="Date",
                    yaxis_title="Price",
                    hovermode="x",
                    separators=".,",
                )

                fig.show()


def show_name(name: str) -> None:
    print(f"Visualizing product with name: {name}")
    data = format_data()

    for category_name, category_info in data.items():
        for product_name, product_info in category_info.items():
            if name == product_name:
                fig = go.Figure()
                for website_name, website_info in product_info.items():
                    fig.add_trace(
                        go.Scatter(
                            name=website_name.capitalize(),
                            x=website_info["dates"],
                            y=website_info["prices"],
                            line={"color": WEBSITE_COLORS[website_name], "width": 2},
                            hovertemplate="Price: %{y:.0f}",
                        )
                    )

                fig.update_traces(mode="markers+lines")
                fig.update_layout(
                    title=f"Price(s) of {product_name.upper()}",
                    xaxis_title="Date",
                    yaxis_title="Price",
                    hovermode="x",
                    separators=".,",
                )

                fig.show()


def show_all_products() -> None:
    print("Visualizing all products")
    data = format_data()

    for category_name, category_info in data.items():
        for product_name, product_info in category_info.items():
            fig = go.Figure()
            for website_name, website_info in product_info.items():
                fig.add_trace(
                    go.Scatter(
                        name=website_name.capitalize(),
                        x=website_info["dates"],
                        y=website_info["prices"],
                        line={"color": WEBSITE_COLORS[website_name], "width": 2},
                        hovertemplate="Price: %{y:.0f}",
                    )
                )

            fig.update_traces(mode="markers+lines")
            fig.update_layout(
                title=f"Price(s) of {product_name.upper()}",
                xaxis_title="Date",
                yaxis_title="Price",
                hovermode="x",
                separators=".,",
            )

            fig.show()


def format_data() -> dict:
    records_data = Filemanager.get_record_data()

    data = {}

    for category_name, category_info in records_data.items():
        data.update({category_name: {}})
        for product_name, product_info in category_info.items():
            data[category_name].update({product_name: {}})

            for website_name, website_info in product_info.items():

                dates = [date for date in website_info["dates"]]
                prices = [website_info["dates"][date]["price"] for date in dates]
                id = website_info["info"]["id"]

                data[category_name][product_name].update(
                    {website_name: {"dates": dates, "prices": prices, "id": id}}
                )

    return data
