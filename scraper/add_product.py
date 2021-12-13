import logging
from scraper.scrape import Scraper
from scraper.filemanager import Filemanager
from scraper.domains import get_website_name, domains


def add_product(category, url) -> None:
    print("Adding product...")
    logger = logging.getLogger(__name__)
    logger.info(f"Adding product: {category} - {url}")

    website_name = get_website_name(url)

    if website_name not in domains.keys():
        print(f"Can't scrape from this website: {website_name}")
        logger.info(f"Not supported website to scrape from: {website_name}")
        return

    new_product = Scraper(category, url)
    new_product.scrape_info()

    product_exists = check_if_product_exits(new_product)

    if not product_exists:
        add_product_to_records(new_product)
        Filemanager.add_product_to_csv(new_product.category, new_product.url)
        new_product.save_info()
    else:
        user_input = input(
            "A product with the same name and from the same website already exist in your data, do you want to override this product? (y/n) > "
        )
        if user_input.lower() in ("y", "yes"):
            print("Overriding product...")
            add_product_to_records(new_product)
            Filemanager.add_product_to_csv(new_product.category, new_product.url)
            new_product.save_info()
        else:
            print("Product was not added nor overrided")
            logger.info("Adding product cancelled")


def check_if_product_exits(product: Scraper) -> bool:
    data = Filemanager.get_record_data()

    # Check category
    if data.get(product.category):
        # Check product name
        if data[product.category].get(product.info.name):
            # Check product website name
            if data[product.category][product.info.name].get(product.website_name):
                return True

    return False


def add_product_to_records(product: Scraper) -> None:
    data = Filemanager.get_record_data()

    if data.get(product.category):
        if data[product.category].get(product.info.name):
            data[product.category][product.info.name].update(
                {product.website_name: {"info": {}, "datapoints": []}}
            )
        else:
            data[product.category].update(
                {
                    product.info.name: {
                        product.website_name: {"info": {}, "datapoints": []}
                    }
                }
            )
    else:
        data.update(
            {
                product.category: {
                    product.info.name: {
                        product.website_name: {"info": {}, "datapoints": []}
                    }
                }
            }
        )

    Filemanager.save_record_data(data)
