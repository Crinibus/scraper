import threading
import logging.config
import logging
import time
import scraper


def main() -> None:
    args = scraper.argparse_setup()

    if args.clean_data:
        scraper.clean_records_data()

    if args.visualize:
        scraper.visualize_data(args.all, args.category, args.id, args.name, args.up_to_date, args.compare)

    if args.reset:
        scraper.reset(args.category, args.name, args.id, args.all)

    if args.add:
        scraper.add_products(args.category, args.url)

    if args.search:
        scraper.search(args.search)

    if args.scrape:
        if args.threads:
            scrape_with_threads()
        else:
            scrape()

    if args.latest_datapoint:
        scraper.print_latest_datapoints(args.name, args.id)

    if args.print_all_products:
        scraper.print_all_products()

    if args.delete:
        scraper.delete(args.category, args.name, args.id, args.all)


def scrape() -> None:
    print("Scraping...")

    request_delay = scraper.Config.get_request_delay()
    products_df = scraper.Filemanager.get_products_data()

    # Create instances of class "Scraper"
    products = [scraper.Scraper(category, url) for category, url in zip(products_df["category"], products_df["url"])]

    # Scrape and save scraped data for each product (sequentially)
    for product in products:
        time.sleep(request_delay)
        product.scrape_info()
        product.save_info()


def scrape_with_threads() -> None:
    print("Scraping with threads...")

    request_delay = scraper.Config.get_request_delay()
    products_df = scraper.Filemanager.get_products_data()

    # Create instances of class "Scraper"
    products = [scraper.Scraper(category, url) for category, url in zip(products_df["category"], products_df["url"])]

    # Create threads
    threads = [threading.Thread(target=product.scrape_info) for product in products]

    # Start scraping on all threads
    for thread in threads:
        time.sleep(request_delay)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Save scraped data for each product (sequentially)
    for product in products:
        product.save_info()


if __name__ == "__main__":
    logging.config.fileConfig(
        fname=scraper.Filemanager.logging_ini_path,
        defaults={"logfilename": scraper.Filemanager.logfile_path},
    )

    main()
