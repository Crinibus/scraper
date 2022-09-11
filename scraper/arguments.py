from argparse import ArgumentParser


def argparse_setup() -> ArgumentParser.parse_args:
    """Setup and return argparse."""
    parser = ArgumentParser(description="")

    parser.add_argument(
        "-s",
        "--scrape",
        help="scrape product info",
        action="store_true",
    )

    parser.add_argument("--threads", help="use threads when scraping product info", action="store_true")

    parser.add_argument(
        "-a",
        "--add",
        help="Add a new product",
        action="store_true",
    )

    parser.add_argument(
        "-c",
        "--category",
        help=(
            "the category(s) the new product is going to be in when using --add "
            "or the category(s) to visualize when using --visualize"
        ),
        type=str,
        nargs="*",
        action="extend",
    )

    parser.add_argument("-u", "--url", help="the url to the product", type=str, nargs="*", action="extend")

    parser.add_argument(
        "-v",
        "--visualize",
        help="visualize your product data",
        action="store_true",
        dest="visualize",
    )

    parser.add_argument(
        "--all",
        help="show all product graphs when used with --visualize",
        action="store_true",
        dest="all",
    )

    parser.add_argument(
        "--id",
        help="show graphs for products with the specified id(s) when used with --visualize",
        type=str,
        nargs="*",
        action="extend",
        dest="id",
    )

    parser.add_argument(
        "-n",
        "--name",
        help="show graphs for product with the specified name(s) when used with --visualize",
        type=str,
        nargs="*",
        action="extend",
        dest="name",
    )

    parser.add_argument(
        "-utd",
        "--up-to-date",
        help="show only graph for a product if the latest product price is today",
        action="store_true",
        dest="up_to_date",
    )

    parser.add_argument(
        "--search",
        help="search for product names with the specified name(s)",
        type=str,
        nargs="*",
        action="extend",
        dest="search",
        metavar="SEARCH_TERM",
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
        "--clean-data",
        help="clean data so unnecessary product datapoints is removed from records",
        action="store_true",
        dest="clean_data",
    )

    parser.add_argument(
        "--latest-datapoint",
        # help="use with --name or --id to print the latest datapoint of the specified product",
        help="use with --visualize-name or --visualize-id to print the latest datapoint of the specified product",
        dest="latest_datapoint",
        action="store_true",
    )

    args = validate_arguments(parser)

    return args


def validate_arguments(parser: ArgumentParser) -> None:
    """Validate arguments"""
    args = parser.parse_args()

    if args.add and args.visualize:
        parser.error("Cannot use --add and --visualize at the same time")

    if args.add:
        if not args.category or not args.url:
            parser.error("When using --add, then --category and --url is required")
        if len(args.category) > len(args.url):
            parser.error("Specified more categories than urls")
        if len(args.category) < len(args.url):
            parser.error("Specified more urls than categories")

    if args.visualize:
        if not any([args.all, args.category, args.id, args.name]):
            parser.error("When using --visualize, then one of the following is required: --all, --category, --id, --name")

    if args.latest_datapoint:
        if not args.name and not args.id:
            parser.error("When using --latest-datapoint, then --name or --id is required")

    return args
