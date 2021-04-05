import logging
from scraper.scrape import Scraper
from scraper.filemanager import Filemanager
from scraper.domains import get_website_name, domains


def add_product(args) -> None:
    print("Adding product...")
    logger = logging.getLogger(__name__)
    logger.info(f"Adding product: {args.category} - {args.url}")

    website_name = get_website_name(args.url)

    if website_name not in domains.keys():
        print(f"Can't scrape from this website: {website_name}")
        logger.info("Not support website to scrape from")
        return

    new_product = Scraper(args.category, args.url)
    new_product.scrape_info()

    is_product_added = add_product_to_records(new_product)

    if is_product_added:
        Filemanager.add_product_to_csv(new_product.category, new_product.url)
        new_product.save_info()
    else:
        logger.info("Adding product cancelled")


def add_product_to_records(product: Scraper) -> bool:
    data = Filemanager.get_record_data()

    category_exist = True if data.get(product.category) else False

    if category_exist:
        product_name_exist = (
            True if data[product.category].get(product.info.name) else False
        )
        if product_name_exist:
            product_and_website_exist = (
                True
                if data[product.category][product.info.name].get(product.website_name)
                else False
            )

            if product_and_website_exist:
                user_input = input(
                    "A product with the same name and from the same website already exist in your data, do you want to override this product? (y/n) > "
                )
                if user_input.lower() in ("n", "no"):
                    print("Product was not overridden")
                    return False

            data[product.category][product.info.name].update(
                {product.website_name: {"info": {}, "dates": {}}}
            )
        else:
            data[product.category].update(
                {product.info.name: {product.website_name: {"info": {}, "dates": {}}}}
            )
    else:
        data.update(
            {
                product.category: {
                    product.info.name: {product.website_name: {"info": {}, "dates": {}}}
                }
            }
        )

    Filemanager.save_record_data(data)
    return True
