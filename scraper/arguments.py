from argparse import ArgumentParser


def argparse_setup() -> ArgumentParser.parse_args:
    """Setup and return argparse."""
    parser = ArgumentParser(description="")

    parser.add_argument(
        "-s",
        "--scrape",
        help="scrape product prices",
        action="store_true",
    )

    parser.add_argument(
        "-a",
        "--add",
        help="Add a product",
        action="store_true",
    )

    parser.add_argument(
        "--reset",
        help="delete data for each product in records.json, such as prices of each recorded day",
        action="store_true",
    )

    parser.add_argument(
        "--hard-reset",
        help="delete all content in records.json and products.csv",
        action="store_true",
    )

    parser.add_argument(
        "-c",
        "--category",
        help="the category the product is going to be in",
        type=str,
        action="append",
    )

    parser.add_argument(
        "-u", "--url", help="the url to the product", type=str, action="append"
    )

    parser.add_argument(
        "--threads", help="use threads when scraping product info", action="store_true"
    )

    parser.add_argument(
        "-v",
        "--visualize",
        help="visualize your data",
        action="store_true",
        dest="visualize",
    )

    parser.add_argument(
        "-va",
        "--visualize-all",
        help="show graph for all products",
        action="store_true",
        dest="show_all",
    )

    parser.add_argument(
        "-vc",
        "--visualize-category",
        help="show graph for the products with the specified categories",
        type=str,
        nargs="*",
        dest="visualize_categories",
        metavar="category",
    )

    parser.add_argument(
        "-id",
        "--visualize-id",
        help="show graph for the products with the specified ids",
        type=str,
        nargs="*",
        dest="visualize_ids",
        metavar="id",
    )

    parser.add_argument(
        "-vn",
        "--visualize-name",
        help="show graph for product with the specified name(s)",
        type=str,
        nargs="*",
        dest="visualize_names",
        metavar="name",
    )

    parser.add_argument(
        "--clean-data",
        help="clean data, so unnecessary datapoints is removed from records",
        action="store_true",
        dest="clean_data",
    )

    validate_arguments(parser)

    return parser.parse_args()


def validate_arguments(parser: ArgumentParser) -> None:
    """Validate arguments"""
    args = parser.parse_args()

    if args.add:
        if not args.category or not args.url:
            parser.error("When using --add, then --category and --url is required")
