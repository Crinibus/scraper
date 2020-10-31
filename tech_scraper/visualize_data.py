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
        type=str
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

    for category in data:
        for product in data[category]:
            dates_1 = []
            prices_1 = []
            dates_2 = []
            prices_2 = []
            domains = []
            for domain in data[category][product]:
                if len(dates_1) == 0:
                    dates_1 = [date for date in data[category][product][domain]['dates']]
                    prices_1 = [int(data[category][product][domain]['dates'][date]['price']) for date in dates_1]
                else:
                    dates_2 = [date for date in data[category][product][domain]['dates']]
                    prices_2 = [int(data[category][product][domain]['dates'][date]['price']) for date in dates_2]

                domains.append(domain)

            # Check for more than one domain
            # If two domains, show both graph for both domains on the same graph
            if len(dates_1) > 0 and len(dates_2) > 0:
                plt.plot(dates_1, prices_1,
                         dates_2, prices_2,
                         marker='o', linestyle='-')
                plt.legend([f'{domains[0]}', f'{domains[1]}'])
            else:
                plt.plot(dates_1, prices_1,
                         marker='o', linestyle='-')
                plt.legend([f'{domains[0]}'])

            plt.style.use('seaborn-darkgrid')
            plt.xticks(rotation=65)
            plt.title(f'Prices of {product.capitalize()}')
            plt.ylabel('Price')
            plt.xlabel('Day')
            plt.show()


def find_partnum(partnum):
    """Show graph with the same partnumber as the argument/parameter partnum"""
    data = read_records()

    dates = []
    prices = []

    for category in data:
        for product in data[category]:
            for domain in data[category][product]:
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


if __name__ == '__main__':
    args = argparse_setup()

    if args.all:
        show_all()
    if args.partnum:
        find_partnum(args.partnum)
