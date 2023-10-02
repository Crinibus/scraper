import threading
import logging.config
import logging
import time
import alive_progress
import scraper

alive_progress.config_handler.set_global(ctrl_c=False, dual_line=True, theme="classic", stats=False)


def main() -> None:
    args = scraper.argparse_setup()

    if args.clean_data:
        scraper.clean_datapoints()

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

    with alive_progress.alive_bar(len(products), title="Scraping") as bar:
        # Scrape and save scraped data for each product (sequentially)
        for product in products:
            bar.text = f"-> {product.url}"
            time.sleep(request_delay)
            product.scrape_info()
            product.save_info()
            bar()


def scrape_with_threads() -> None:
    print("Scraping with threads...")

    request_delay = scraper.Config.get_request_delay()

    products_df = scraper.Filemanager.get_products_data()
    domain_grouped_products_df = scraper.get_products_df_grouped_by_domains(products_df)
    grouped_products = scraper.get_products_grouped_by_domain(domain_grouped_products_df)

    grouped_scraper_threads: list[list[threading.Thread]] = []

    # Create scraper threads and group by domain
    for products in grouped_products.values():
        scraper_threads = [threading.Thread(target=product.scrape_info) for product in products]
        grouped_scraper_threads.append(scraper_threads)

    products_flatten = [product for products in grouped_products.values() for product in products]

    with alive_progress.alive_bar(len(products_flatten), title="Scraping with threads") as progress_bar:
        # Create master threads to manage scraper threads sequentially for each domain
        master_threads = [
            threading.Thread(target=scraper.start_threads_sequentially, args=[scraper_threads, request_delay, progress_bar])
            for scraper_threads in grouped_scraper_threads
        ]

        # Start all master threads
        for master_thread in master_threads:
            master_thread.start()

        # Wait for all master threads to finish
        for master_thread in master_threads:
            master_thread.join()

    # Save scraped data for each product (sequentially)
    for product in products_flatten:
        product.save_info()


if __name__ == "__main__":
    logging.config.fileConfig(
        fname=scraper.Filemanager.logging_ini_path,
        defaults={"logfilename": scraper.Filemanager.logfile_path},
    )

    main()
