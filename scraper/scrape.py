import requests
from bs4 import BeautifulSoup
from datetime import datetime
from scraper.constants import REQUEST_HEADER, REQUEST_COOKIES
from scraper.domains import Info, domains, get_website_name
from scraper.filemanager import Logger, Filemanager
from scraper.format import Format


class Scraper:
    def __init__(self, category: str, url: str) -> None:
        self.category = category
        self.url = url
        self.website_name = get_website_name(url)
        self.info = Info
        self.logger = Logger.create_logger("Scraper")

    def scrape_info(self) -> None:
        soup = self.request_url()
        self.get_info(soup)

    def request_url(self) -> BeautifulSoup:
        response = requests.get(self.url, headers=REQUEST_HEADER, cookies=REQUEST_COOKIES)
        return BeautifulSoup(response.text, "html.parser")

    def get_info(self, soup: BeautifulSoup) -> None:
        domain_function = domains.get(self.website_name)
        self.info = domain_function(soup)

    def save_info(self) -> None:
        data = self.update_data()
        Filemanager.save_record_data(data)

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
