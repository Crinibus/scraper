from scraper.scrape import Scraper
from scraper.filemanager import Filemanager


def add_product(args):
    print("Adding product...")

    new_product = Scraper(args.category, args.url)
    new_product.scrape_info()

    data = Filemanager.get_record_data()

    data.update(
        {
            args.category: {
                new_product.info.name: {
                    new_product.website_name: {"info": {}, "dates": {}}
                }
            }
        }
    )

    Filemanager.save_record_data(data)

    new_product.save_info()
