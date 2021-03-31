import pandas as pd
import threading
import logging.config
import scraper


def main():
    args = scraper.argparse_setup()

    if args.reset:
        reset()

    if args.add:
        scraper.add_product(args)

    if args.scrape:
        scrape()


def scrape():
    print("Scraping...")

    products_df = pd.read_csv("./scraper/products.csv", sep=",", header=0)

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
    pass


if __name__ == "__main__":
    logging.config.fileConfig(fname="scraper/logging.ini")
    main()
