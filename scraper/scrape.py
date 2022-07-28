import requests
from bs4 import BeautifulSoup
from datetime import datetime
from scraper.constants import REQUEST_HEADER, REQUEST_COOKIES
from scraper.domains import get_website_handler
from scraper.filemanager import Filemanager
from scraper.format import Format, Info
import logging


class Scraper:
    def __init__(self, category: str, url: str) -> None:
        self.category = category
        self.url = url
        self.website_handler = get_website_handler(url)
        self.product_info: Info

    def scrape_info(self) -> None:
        logging.getLogger(__name__).debug(f"Scraping: {self.category} - {self.url}")
        soup = request_url(self.url)
        self.product_info = self.website_handler.get_product_info(soup)

    def save_info(self) -> None:
        if not self.product_info or not self.product_info.valid:
            print(f"Product info is not valid - category: '{self.category}' - url: {self.url}")
            return

        save_product(self.category, self.url, self.website_handler.website_name, self.product_info)

    def print_info(self) -> None:
        print(f"\nCategory: {self.category}")
        print(f"URL: {self.url}")
        print(f"Website: {self.website_handler.website_name}")
        print(f"Product name: {self.product_info.name}")
        print(f"Product price: {self.product_info.price}")
        print(f"Product currency: {self.product_info.currency}")
        print(f"Product id: {self.product_info.id}")
        print(f"Product valid: {self.product_info.valid}")


def request_url(url: str) -> BeautifulSoup:
    try:
        response = requests.get(url, headers=REQUEST_HEADER, cookies=REQUEST_COOKIES, timeout=10)
        return BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.RequestException:  # temporary try expect for all requests errors
        logging.getLogger(__name__).exception(f"Module requests exception with url: {url}")


def save_product(category: str, url: str, website_name: str, product_info: Info) -> None:
    data = Filemanager.get_record_data()

    product_data = get_product_data(data, category, product_info.name, website_name)

    if not product_data:
        return

    short_url = Format.shorten_url(website_name, url, product_info)
    product_data["info"].update({"url": short_url, "id": product_info.id, "currency": product_info.currency})

    # doesn't return anything because the function mutates the dictionary in the variable 'product_data',
    # which is a part of the dictionary in the variable 'data'
    add_product_datapoint(product_data, product_info.price)

    # save the dictionary in the variable 'data' because it has been mutated with the new datapoint of the product
    Filemanager.save_record_data(data)


def get_product_data(data: dict, category: str, name: str, website_name: str) -> dict:
    try:
        product_data = data[category][name][website_name]
        return product_data
    except KeyError:
        logging.getLogger(__name__).exception(
            f"KeyError on dict 'data' with category: '{category}', name: '{name}' and website_name: '{website_name}'"
        )
        return None


def add_product_datapoint(product_data: dict, price: float) -> None:
    date = datetime.today().strftime("%Y-%m-%d")
    product_datapoints = product_data["datapoints"]

    new_datapoint = {"date": date, "price": price}

    if len(product_datapoints) == 0:
        product_datapoints.append(new_datapoint)
        return

    latest_datapoint = product_datapoints[-1]
    if latest_datapoint["date"] == date:
        latest_datapoint["price"] = price
    else:
        product_datapoints.append(new_datapoint)
