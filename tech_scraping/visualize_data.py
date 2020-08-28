import json
import matplotlib.pyplot as plt
import argparse


def argparse_setup():
    """Setup and return argparse."""
    parser = argparse.ArgumentParser()

    # optional argument
    parser.add_argument('--all',
                        help='Show graphs for all products',
                        action="store_true")

    return parser.parse_args()


def read_records():
    """Read and return data from records.json."""
    with open('records.json', 'r') as jsonfile:
        data = json.load(jsonfile)

    return data


def asus_2080ti():
    """Show graph for ASUS RTX 2080 TI ROG Strix graphics cards."""
    data = read_records()

    # Get dates
    komplett_dates = [date for date in data['gpu']['asus geforce rtx 2080 ti rog strix oc']['www.komplett.dk']['dates']]
    proshop_dates = [date for date in data['gpu']['asus geforce rtx 2080 ti rog strix oc']['www.proshop.dk']['dates']]

    # Get prices
    komplett_prices = [int(data['gpu']['asus geforce rtx 2080 ti rog strix oc']['www.komplett.dk']['dates'][date]['price']) for date in komplett_dates]
    proshop_prices = [int(data['gpu']['asus geforce rtx 2080 ti rog strix oc']['www.proshop.dk']['dates'][date]['price']) for date in proshop_dates]

    # Plotting
    plt.plot(komplett_dates, komplett_prices,
             proshop_dates, proshop_prices,
             marker='o', linestyle='-')

    # Styling
    plt.style.use('seaborn-darkgrid')
    plt.title('Prices of ASUS 2080 TI ROG Strix')
    plt.xlabel('Day')
    plt.ylabel('Price')
    plt.xticks(rotation=70)
    plt.legend(['Komplett', 'Proshop'])

    # Show graph
    plt.show()


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


if __name__ == '__main__':
    args = argparse_setup()

    if args.all:
        show_all()
    else:
        asus_2080ti()
