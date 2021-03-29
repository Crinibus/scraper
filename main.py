import pandas as pd
import threading
from scraper import Scraper


def main():
    products_df = pd.read_csv("./scraper/products.csv", sep=",", header=0)

    # Create instances of class "Scraper"
    # products = [
    #     Scraper(data["category"], data["url"]) for _, data in products_df.iterrows()
    # ]

    # Create instances of class "Scraper"
    products = [
        Scraper(category, url) for category, url in zip(products_df["category"], products_df["url"])
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


if __name__ == "__main__":
    main()
