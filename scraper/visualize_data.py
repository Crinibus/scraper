import json
from argparse import ArgumentParser
import plotly.graph_objs as go


def argparse_setup() -> ArgumentParser:
    """Setup and return argparse."""
    parser = ArgumentParser()

    # optional argument
    parser.add_argument(
        '--all',
        help='Show graphs for all products',
        action="store_true"
    )

    # optional argument
    parser.add_argument(
        '-p',
        '--partnum',
        help='Show graph for only the product with the specified partnumber',
        action='append'
    )

    # optional argument
    parser.add_argument(
        '-c',
        '--category',
        help='Show graph for only the products with the specified category',
        action='append'
    )

    return parser.parse_args()


def read_records() -> dict:
    """Read and return data from records.json."""
    with open('records.json', 'r') as jsonfile:
        data = json.load(jsonfile)

    return data


def show_all():
    """Show graphs for all products."""
    data = read_records()

    visu_data = {}

    for category in data:
        for product in data[category]:
            visu_data[product] = {}
            partnumbers = []

            for domain in data[category][product]:
                # Add keys under domain in product
                visu_data[product][domain] = {'dates': [], 'prices': []}

                # Get dates, prices and partnumber
                dates = [date for date in data[category][product][domain]['dates']]
                prices = [int(data[category][product][domain]['dates'][date]['price']) for date in dates]
                partnumber = data[category][product][domain]['info']['part_num']

                # Save dates, prices and partnumber
                visu_data[product][domain]['dates'] = dates
                visu_data[product][domain]['prices'] = prices
                partnumbers.append(partnumber)

            # Plotly figure
            fig = go.Figure()

            # List with colors for graph lines
            colors = ['aqua', 'red', 'green']

            # Make a graph for the product with all it's domains
            for index, domain in enumerate(visu_data[product].keys()):

                fig.add_trace(go.Scatter(
                    x=list(visu_data[product][domain]['dates']),
                    y=list(visu_data[product][domain]['prices']),
                    name=domain,
                    line=dict(color=colors[index], width=2),
                    hovertemplate='Price: %{y:.0f}'
                ))

            fig.update_traces(mode='markers+lines')
            fig.update_layout(
                title=f'Prices of {product.capitalize()} -> Partnumber(s): {", ".join(partnumbers)}',
                xaxis_title='Date',
                yaxis_title='Price',
                hovermode='x',
                separators='.,'
            )

            fig.show()


def find_partnum(partnum: str):
    """Show graph for the product with the same partnumber as the argument/parameter partnum"""
    data = read_records()

    dates = []
    prices = []

    for category in data:
        for product in data[category]:
            for domain in data[category][product]:
                # Get partnumber
                part_num = data[category][product][domain]['info']['part_num']

                if part_num == partnum:
                    # Get dates and prices for the product
                    dates = [date for date in data[category][product][domain]['dates']]
                    prices = [int(data[category][product][domain]['dates'][date]['price']) for date in dates]

                    # Plotly figure
                    fig = go.Figure()

                    # Color of graph line
                    _color = 'red'

                    # Make graph
                    fig.add_trace(go.Scatter(
                        x=dates,
                        y=prices,
                        name=domain,
                        line=dict(color=_color, width=2),
                        hovertemplate='Price: %{y:.0f}'
                    ))

                    fig.update_traces(mode='markers+lines')
                    fig.update_layout(
                        title=f'Prices of {product.capitalize()} -> Partnumber: {part_num}',
                        xaxis_title='Date',
                        yaxis_title='Price',
                        hovermode='x',
                        separators='.,'
                    )

                    fig.show()
                    return
    print('Couldn\'t find the specified partnumber in records.json')


def find_category(_category: str):
    data = read_records()

    visu_data = {}

    for category in data:
        if category == _category:
            for product in data[category]:
                visu_data[product] = {}
                partnumbers = []

                for domain in data[category][product]:
                    # Add keys under domain in product
                    visu_data[product][domain] = {'dates': [], 'prices': []}

                    # Get dates, prices and partnumber
                    dates = [date for date in data[category][product][domain]['dates']]
                    prices = [int(data[category][product][domain]['dates'][date]['price']) for date in dates]
                    partnumber = data[category][product][domain]['info']['part_num']

                    # Save dates, prices and partnumber
                    visu_data[product][domain]['dates'] = dates
                    visu_data[product][domain]['prices'] = prices
                    partnumbers.append(partnumber)

                # Plotly figure
                fig = go.Figure()

                # List with colors for graph lines
                colors = ['aqua', 'red', 'green']

                # Make a graph for the product with all it's domains
                for index, domain in enumerate(visu_data[product].keys()):

                    fig.add_trace(go.Scatter(
                        x=list(visu_data[product][domain]['dates']),
                        y=list(visu_data[product][domain]['prices']),
                        name=domain,
                        line=dict(color=colors[index], width=2),
                        hovertemplate='Price: %{y:.0f}'
                    ))

                fig.update_traces(mode='markers+lines')
                fig.update_layout(
                    title=f'Prices of {product.capitalize()} -> Partnumber(s): {", ".join(partnumbers)}',
                    xaxis_title='Date',
                    yaxis_title='Price',
                    hovermode='x',
                    separators='.,'
                )

                fig.show()
        else:
            continue


if __name__ == '__main__':
    args = argparse_setup()

    if args.all:
        show_all()
    if args.partnum:
        for partnum in args.partnum:
            find_partnum(partnum)

    if args.category:
        for category in args.category:
            find_category(category)
