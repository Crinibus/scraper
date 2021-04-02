import requests
from bs4 import BeautifulSoup
from datetime import datetime
from scraper.constants import REQUEST_HEADER, REQUEST_COOKIES
from scraper.domains import domains, get_website_name
from scraper.filemanager import Filemanager
from scraper.format import Format, Info
import logging


class Scraper:
    def __init__(self, category: str, url: str) -> None:
        self.category = category
        self.url = url
        self.website_name = get_website_name(url)
        self.info = Info
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"Instantiating Scraper: {self.category} - {self.url}")

    def scrape_info(self) -> None:
        soup = Scraper.request_url(self.url)
        self.get_info(soup)

    @staticmethod
    def request_url(url: str) -> BeautifulSoup:
        response = requests.get(url, headers=REQUEST_HEADER, cookies=REQUEST_COOKIES)
        return BeautifulSoup(response.text, "html.parser")

    def get_info(self, soup: BeautifulSoup) -> None:
        domain_function = domains.get(self.website_name)
        self.info = domain_function(soup)

    def save_info(self) -> None:
        data = self.update_data()
        Filemanager.save_record_data(data)
        self.logger.debug(f"Saving info: {self.category} - {self.url}")

    def update_data(self) -> dict:
        short_url = Format.shorten_url(self.website_name, self.url, self.info)
        date = datetime.today().strftime('%Y-%m-%d')
        data = Filemanager.get_record_data()

        product_info = data[self.category][self.info.name][self.website_name]

        # Get product id either from info.partnum or info.asin (only Amazon)
        product_id = self.info.partnum if self.info.partnum else self.info.asin

        product_info["info"].update({"url": short_url, "id": product_id})
        product_info["dates"].update({date: {"price": self.info.price}})

        return data
