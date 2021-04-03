from scraper.filemanager import Filemanager
import threading
# import logging.config
import logging
import scraper


def main():
    args = scraper.argparse_setup()

    if args.reset:
        reset()

    if args.hard_reset:
        hard_reset()
        Filemanager.clear_product_csv()

    if args.add:
        scraper.add_product(args)

    if args.scrape:
        scrape()


def scrape():
    print("Scraping...")

    products_df = scraper.Filemanager.get_products_data()

    # Create instances of class "Scraper"
    products = [
        scraper.Scraper(category, url) for category, url in zip(products_df["category"], products_df["url"])
    ]

    # Create threads
    threads = [
        threading.Thread(target=product.scrape_info) for product in products
    ]

    # Start scraping on all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Save scraped data for each product (sequentially)
    for product in products:
        product.save_info()


def reset():
    print("Resetting data...")
    logging.getLogger(__name__).info("Resetting data")

    data = scraper.Filemanager.get_record_data()

    for category in data.values():
        for product in category.values():
            for website in product.values():
                website["info"] = {"id": "", "url": ""}
                website["dates"] = {}

    scraper.Filemanager.save_record_data(data)


def hard_reset():
    print("Hard resetting data...")
    logging.getLogger(__name__).info("Hard resetting data")

    data = {}
    scraper.Filemanager.save_record_data(data)
    scraper.Filemanager.clear_product_csv()


if __name__ == "__main__":
    logfile_path = f"{Filemanager.get_root_path()}\\scraper\\logfile.log"

    logging.config.fileConfig(
        fname=f"{Filemanager.get_root_path()}/scraper/logging.ini",
        defaults={"logfilename": f"{Filemanager.get_root_path()}/scraper/logfile.log"}
    )

    main()
