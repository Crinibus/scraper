import threading
import logging.config
import logging
import scraper


def main():
    args = scraper.argparse_setup()

    if args.clean_data:
        scraper.clean_data()

    if args.visualize:
        visualize(args)

    if args.reset:
        reset()

    if args.hard_reset:
        hard_reset()

    if args.add:
        add_products(args)

    if args.scrape:
        if args.threads:
            scrape_with_threads()
        else:
            scrape()


def scrape():
    print("Scraping...")

    products_df = scraper.Filemanager.get_products_data()

    # Create instances of class "Scraper"
    products = [
        scraper.Scraper(category, url) for category, url in zip(products_df["category"], products_df["url"])
    ]

    # Scrape and save scraped data for each product (sequentially)
    for product in products:
        product.scrape_info()
        product.save_info()


def scrape_with_threads():
    print("Scraping with threads...")

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


def add_products(args):
    for category, url in zip(args.category, args.url):
        scraper.add_product(category, url)


def visualize(args):
    print("Visualizing...")
    if args.show_all:
        scraper.show_all_products()

    if args.visualize_categories:
        for category in args.visualize_categories:
            scraper.show_category(category)

    if args.visualize_ids:
        for id in args.visualize_ids:
            scraper.show_id(id)

    if args.visualize_names:
        for name in args.visualize_names:
            scraper.show_name(name)


def reset():
    print("Resetting data...")
    logging.getLogger(__name__).info("Resetting data")

    data = scraper.Filemanager.get_record_data()

    for category in data.values():
        for product in category.values():
            for website in product.values():
                website["info"] = {"id": "", "url": "", "currency": ""}
                website["datapoints"] = []

    scraper.Filemanager.save_record_data(data)


def hard_reset():
    print("Hard resetting data...")
    logging.getLogger(__name__).info("Hard resetting data")

    data = {}
    scraper.Filemanager.save_record_data(data)
    scraper.Filemanager.clear_product_csv()


if __name__ == "__main__":
    logging.config.fileConfig(
        fname=f"{scraper.Filemanager.root_path}/scraper/logging.ini",
        defaults={"logfilename": f"{scraper.Filemanager.root_path}/scraper/logfile.log"}
    )

    main()
