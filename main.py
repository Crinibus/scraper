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

    if args.activate:
        scraper.update_products_is_active_with_product_codes(args.id, True)

    if args.deactivate:
        scraper.update_products_is_active_with_product_codes(args.id, False)

    if args.search:
        scraper.search(args.search)

    if args.scrape:
        if args.threads:
            scrape_with_threads()
        else:
            scrape()

    if args.latest_datapoint:
        scraper.print_latest_datapoints(args.name, args.id, args.category)

    if args.list_products:
        if any([args.name, args.id, args.category]):
            scraper.list_products_with_filters(args.name, args.id, args.category)
        else:
            scraper.print_all_products()

    if args.delete:
        scraper.delete(args.category, args.name, args.id, args.all)


def scrape() -> None:
    print("Scraping...")

    request_delay = scraper.Config.get_request_delay()
    active_products = scraper.db.get_all_products(select_only_active=True)

    products = scraper.Format.db_products_to_scrapers(active_products)

    with alive_progress.alive_bar(len(products), title="Scraping") as bar:
        # Scrape and save scraped data for each product (sequentially)
        for product in products:
            bar.text = f"-> {product.url}"
            time.sleep(request_delay)
            product.scrape_info()
            scraper.add_product.add_new_datapoint_with_scraper(product)
            bar()


def scrape_with_threads() -> None:
    print("Scraping with threads...")

    request_delay = scraper.Config.get_request_delay()

    grouped_db_products = scraper.db.get_all_products_grouped_by_domains(select_only_active=True)
    grouped_products: list[list[scraper.Scraper]] = []

    for db_products in grouped_db_products:
        products = scraper.Format.db_products_to_scrapers(db_products)
        grouped_products.append(products)

    grouped_scraper_threads: list[list[threading.Thread]] = []

    # Create scraper threads and group by domain
    for products in grouped_products:
        scraper_threads = [threading.Thread(target=product.scrape_info) for product in products]
        grouped_scraper_threads.append(scraper_threads)

    products_flatten = [product for products in grouped_products for product in products]

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
        scraper.add_product.add_new_datapoint_with_scraper(product)


if __name__ == "__main__":
    scraper.db.create_db_and_tables()
    logging.config.fileConfig(
        fname=scraper.Filemanager.logging_ini_path,
        defaults={"logfilename": scraper.Filemanager.logfile_path},
    )

    main()
