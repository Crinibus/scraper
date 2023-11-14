import time
import threading
import logging

from scraper.models import Info
from scraper.domains import get_website_handler


class Scraper:
    def __init__(self, category: str, url: str) -> None:
        self.category = category
        self.url = url
        self.website_handler = get_website_handler(url)
        self.product_info: Info = None

    def scrape_info(self) -> Info:
        logging.getLogger(__name__).debug(f"Scraping: {self.category} - {self.url}")
        self.product_info = self.website_handler.get_product_info()
        return self.product_info


def start_threads_sequentially(threads: list[threading.Thread], request_delay: int, progress_bar=None) -> None:
    for thread in threads:
        thread.start()
        thread.join()
        time.sleep(request_delay)

        if progress_bar:
            progress_bar()
