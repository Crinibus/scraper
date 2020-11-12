import json
import matplotlib.pyplot as plt
import argparse


def argparse_setup():
    """Setup and return argparse."""
    parser = argparse.ArgumentParser()

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


def read_records():
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
                visu_data[product][domain]['dates'] = [date for date in data[category][product][domain]['dates']]
                visu_data[product][domain]['prices'] = [int(data[category][product][domain]['dates'][date]['price']) for date in visu_data[product][domain]['dates']]
                partnumbers.append(data[category][product][domain]['info']['part_num'])

            # Make a graph for the product with all it's domains
            for domain in visu_data[product].keys():
                plt.plot(list(visu_data[product][domain]['dates']),
                         list(visu_data[product][domain]['prices']),
                         marker='o',
                         linestyle='-')

            plt.legend(list(visu_data[product].keys()))
            plt.style.use('seaborn-darkgrid')
            plt.xticks(rotation=65)
            plt.title(f'Prices of {product.capitalize()}\n'
                      f'Partnumber(s): {", ".join(partnumbers)}')
            plt.ylabel('Price')
            plt.xlabel('Day')
            plt.show()


def find_partnum(partnum):
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

                    # Plot graph
                    plt.plot(dates, prices, marker='o', linestyle='-')
                    plt.legend([domain])
                    plt.style.use('seaborn-darkgrid')
                    plt.xticks(rotation=65)
                    plt.title(f'Prices of {product.capitalize()}')
                    plt.ylabel('Price')
                    plt.xlabel('Day')
                    plt.show()
                    return
    print('Couldn\'t find the specified partnumber in records.json')


def find_category(_category):
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
                    visu_data[product][domain]['dates'] = [date for date in data[category][product][domain]['dates']]
                    visu_data[product][domain]['prices'] = [int(data[category][product][domain]['dates'][date]['price']) for date in visu_data[product][domain]['dates']]
                    partnumbers.append(data[category][product][domain]['info']['part_num'])

                # Make a graph for the product with all it's domains
                for domain in visu_data[product].keys():
                    plt.plot(list(visu_data[product][domain]['dates']),
                             list(visu_data[product][domain]['prices']),
                             marker='o',
                             linestyle='-')

                plt.legend(list(visu_data[product].keys()))
                plt.style.use('seaborn-darkgrid')
                plt.xticks(rotation=65)
                plt.title(f'Prices of {product.capitalize()}\n'
                          f'Partnumber(s): {", ".join(partnumbers)}')
                plt.ylabel('Price')
                plt.xlabel('Day')
                plt.show()
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
