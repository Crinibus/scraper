import argparse


def argparse_setup() -> argparse.Namespace:
    """Setup and return argparse."""
    parser = argparse.ArgumentParser(description="")

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
        help="specify category(s)",
        type=str,
        nargs="*",
        action="extend",
        default=[],
    )

    parser.add_argument("-u", "--url", help="the url to the product", type=str, nargs="*", action="extend")

    parser.add_argument("--activate", help="activate a product to be scraped", action="store_true")

    parser.add_argument("--deactivate", help="deactivate a product to not be scraped", action="store_true")

    parser.add_argument(
        "-v",
        "--visualize",
        help="visualize your product data",
        action="store_true",
        dest="visualize",
    )

    parser.add_argument(
        "--all",
        help="specify all products",
        action="store_true",
        dest="all",
    )

    parser.add_argument(
        "--id",
        help="specify id(s) of product(s)",
        type=str,
        nargs="*",
        action="extend",
        dest="id",
        default=[],
    )

    parser.add_argument(
        "-n",
        "--name",
        help="specify names(s) of product(s)",
        type=str,
        nargs="*",
        action="extend",
        dest="name",
        default=[],
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
        "--compare",
        help="compare two or more products",
        action="store_true",
        dest="compare",
    )

    parser.add_argument(
        "--reset",
        help="delete data for each product in records.json, such as prices of each recorded day",
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
        help="get the latest datapoint of specified product(s)",
        dest="latest_datapoint",
        action="store_true",
    )

    parser.add_argument(
        "--list-products",
        help="lists the names, websites and ids of all products",
        dest="list_products",
        action="store_true",
    )

    parser.add_argument(
        "--delete",
        help="delete all or specific products or categories",
        dest="delete",
        action="store_true",
    )

    args = validate_arguments(parser)

    return args


def validate_arguments(parser: argparse.ArgumentParser) -> argparse.Namespace:
    """Validate arguments"""
    args = parser.parse_args()

    if args.add and args.visualize:
        parser.error("Cannot use --add and --visualize at the same time")

    if args.activate and args.deactivate:
        parser.error("Cannot use --activate and --deactivate at the same time")

    if (args.activate or args.deactivate) and not args.id:
        parser.error("When using --activate or --deactivate, then --id is required")

    if args.delete:
        if args.all and any([args.category, args.name, args.id]):
            parser.error("When using --delete and --all, then using --category, --name or --id does nothing")

    if args.add:
        if not args.category or not args.url:
            parser.error("When using --add, then --category and --url is required")
        if len(args.category) > len(args.url):
            parser.error("Specified more categories than urls")
        if len(args.category) < len(args.url):
            parser.error("Specified more urls than categories")

    if args.visualize:
        if not any([args.all, args.category, args.id, args.name, args.compare]):
            parser.error(
                "When using --visualize, then one of the following is required: --all, --category, --id, --name, --compare"
            )
        if args.compare and not any([args.id, args.name, args.category, args.all]):
            parser.error(
                "When using --visualize and --compare, then one of the following is required: --id, --name, --category, --all"
            )

    if args.latest_datapoint:
        if not any([args.name, args.id, args.category]):
            parser.error("When using --latest-datapoint, then --name, --id or --category is required")

    return args
