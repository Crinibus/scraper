import requests
from bs4 import BeautifulSoup
from datetime import datetime
from scraper.constants import REQUEST_HEADER, REQUEST_COOKIES
from scraper.filemanager import Filemanager
from scraper.format import Format, Info
import logging
import json

from abc import ABC, abstractmethod

# ------------------------------ FILE: scrape.py ------------------------------
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


# ------------------------------ FILE: domains.py ------------------------------
class BaseWebsiteHandler(ABC):
    def __init__(self, url: str) -> None:
        # super().__init__()
        self.url = url
        self.website_name = get_website_name(url)

    def get_product_info(self, soup: BeautifulSoup) -> Info:
        try:
            name = self._get_product_name(soup)
            price = self._get_product_price(soup)
            currency = self._get_product_currency(soup)
            id = self._get_product_id(soup)
            return Info(name, price, currency, id)
        except (AttributeError, ValueError):
            logging.getLogger(__name__).exception(f"Could not get all the data needed from url: {self.url}")
            return Info(None, None, None, None, valid=False)

    @abstractmethod
    def _get_product_name(self, soup: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def _get_product_price(self, soup: BeautifulSoup) -> float:
        pass

    @abstractmethod
    def _get_product_currency(self, soup: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def _get_product_id(self, soup: BeautifulSoup) -> str:
        pass


class KomplettHandler(BaseWebsiteHandler):
    def _get_product_name(self, soup: BeautifulSoup) -> str:
        product_name = soup.find("div", class_="product-main-info__info").h1.span.text.lower()
        name = Format.get_user_product_name(product_name)
        return name

    def _get_product_price(self, soup: BeautifulSoup) -> float:
        return float(soup.find("span", class_="product-price-now").text.strip(",-").replace(".", ""))

    def _get_product_currency(self, soup: BeautifulSoup) -> str:
        script_tag = soup.find("script", type="application/ld+json").contents[0]
        currency = json.loads(script_tag).get("offers").get("priceCurrency")
        return currency

    def _get_product_id(self, soup: BeautifulSoup) -> str:
        return soup.find("span", itemprop="sku").text


class ProshopHandler(BaseWebsiteHandler):
    def _get_product_name(self, soup: BeautifulSoup) -> str:
        return "proshop-name-test"

    def _get_product_price(self, soup: BeautifulSoup) -> float:
        return 32

    def _get_product_currency(self, soup: BeautifulSoup) -> str:
        return "dkk-test"

    def _get_product_id(self, soup: BeautifulSoup) -> str:
        return "proshop-id-test"


def get_website_handler(url: str) -> BaseWebsiteHandler:
    website_name = get_website_name(url).lower()

    match website_name:
        case "komplett":
            return KomplettHandler(url)
        case "proshop":
            return ProshopHandler(url)
        case _:
            logging.getLogger(__name__).error(
                f"Can't find a website handler - website: '{website_name}' possibly not supported"
            )
            return None


def get_website_name(url: str) -> str:
    domain = url.split("/")[2]

    # Remove "www." and the TLD/DNS name (such as ".com")
    website_name_list = domain.strip("www.").split(".")[:-1]
    website_name = ".".join(website_name_list)
    return website_name
