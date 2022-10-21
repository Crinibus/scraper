import threading
import logging.config
import logging
import time
import alive_progress
import scraper

alive_progress.config_handler.set_global(ctrl_c=False, dual_line=True, theme="classic", stats=False)


def main():
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


def scrape():
    print("Scraping...")

    request_delay = scraper.Config.get_request_delay()
    products_df = scraper.Filemanager.get_products_data()

    # Create instances of class "Scraper"
    products = [scraper.Scraper(category, url) for category, url in zip(products_df["category"], products_df["url"])]

    # Scrape and save scraped data for each product (sequentially)
    # for product in products:
    #     time.sleep(request_delay)
    #     product.scrape_info()
    #     product.save_info()

    with alive_progress.alive_bar(len(products), title="Scraping") as bar:
        # Scrape and save scraped data for each product (sequentially)
        for product in products:
            bar.text = f"-> {product.url}"
            time.sleep(request_delay)
            product.scrape_info()
            product.save_info()
            bar()


def scrape_with_threads():
    print("Scraping with threads...")

    request_delay = scraper.Config.get_request_delay()
    products_df = scraper.Filemanager.get_products_data()

    # Create instances of class "Scraper"
    products = [scraper.Scraper(category, url) for category, url in zip(products_df["category"], products_df["url"])]

    # Create threads
    threads = [threading.Thread(target=product.scrape_info) for product in products]

    with alive_progress.alive_bar(len(products), title="Scraping") as bar:
        # Start scraping on all threads
        for thread in threads:
            time.sleep(request_delay)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()
            bar()

    # Save scraped data for each product (sequentially)
    for product in products:
        product.save_info()


if __name__ == "__main__":

    # DON'T MERGE WITH MASTER BRANCH: KNOWN ISSUE: https://github.com/rsalmei/alive-progress/issues/155
    # alive_progress crashes with the below logging config settings
    logging.config.fileConfig(
        fname=scraper.Filemanager.logging_ini_path,
        defaults={"logfilename": scraper.Filemanager.logfile_path},
    )

    main()
