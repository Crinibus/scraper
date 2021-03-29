from argparse import ArgumentParser


def argparse_setup() -> ArgumentParser.parse_args:
    """Setup and return argparse."""
    parser = ArgumentParser()

    parser.add_argument(
        "-c", "--category", help="the category the product is going to be in", type=str
    )

    parser.add_argument("-u", "--url", help="the url to the product", type=str)

    parser.add_argument(
        "--komplett",
        help="add only komplett-domain under the product-name,"
        "if this is the only optional flag",
        action="store_true",
    )

    parser.add_argument(
        "--proshop",
        help="add only proshop-domain under the product-name,"
        "if this is the only optional flag",
        action="store_true",
    )

    parser.add_argument(
        "--computersalg",
        help="add only computersalg-domain under the product-name,"
        "if this is the only optional flag",
        action="store_true",
    )

    parser.add_argument(
        "--elgiganten",
        help="add only elgiganten-domain under the product-name,"
        "if this is the only optional flag",
        action="store_true",
    )

    parser.add_argument(
        "--avxperten",
        help="add only avxperten-domain under the product-name,"
        "if this is the only optional flag",
        action="store_true",
    )

    parser.add_argument(
        "--avcables",
        help="add only avcables-domain under the product-name,"
        "if this is the only optional flag",
        action="store_true",
    )

    parser.add_argument(
        "--amazon",
        help="add only amazon-domain under the product-name,"
        "if this is the only optional flag",
        action="store_true",
    )

    parser.add_argument(
        "--ebay",
        help="add only ebay-domain under the product-name,"
        "if this is the only optional flag",
        action="store_true",
    )

    parser.add_argument(
        "--power",
        help="add only power-domain under the product-name,"
        "if this is the only optional flag",
        action="store_true",
    )

    parser.add_argument(
        "--expert",
        help="add only expert-domain under the product-name,"
        "if this is the only optional flag",
        action="store_true",
    )

    parser.add_argument(
        "--mmvision",
        help="add only mm-vision-domain under the product-name,"
        "if this is the only optional flag",
        action="store_true",
    )

    parser.add_argument(
        "--coolshop",
        help="add only coolshop-domain under the product-name,"
        "if this is the only optional flag",
        action="store_true",
    )

    parser.add_argument(
        "--sharkgaming",
        help="add only sharkgaming-domain under the product-name,"
        "if this is the only optional flag",
        action="store_true",
    )

    validate_arguments(parser)

    return parser.parse_args()


def validate_arguments(parser: ArgumentParser) -> None:
    """Validate arguments"""
    args = parser.parse_args()

    if args.category and not args.url:
        parser.error("When using --category, then --url is required")
