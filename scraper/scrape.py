from datetime import datetime
from scraper.domains import BaseWebsiteHandler, get_website_handler
from scraper.filemanager import Filemanager
from scraper.format import Info
import logging


class Scraper:
    def __init__(self, category: str, url: str) -> None:
        self.category = category
        self.url = url
        self.website_handler = get_website_handler(url)
        self.product_info: Info

    def scrape_info(self) -> None:
        logging.getLogger(__name__).debug(f"Scraping: {self.category} - {self.url}")
        self.product_info = self.website_handler.get_product_info()

    def save_info(self) -> None:
        if not self.product_info or not self.product_info.valid:
            print(f"Product info is not valid - category: '{self.category}' - url: {self.url}")
            return

        save_product(self.category, self.url, self.website_handler, self.product_info)


def save_product(category: str, url: str, website_handler: BaseWebsiteHandler, product_info: Info) -> None:
    data = Filemanager.get_record_data()

    product_data = get_product_data(data, category, product_info.name, website_handler.website_name)

    if not product_data:
        return

    short_url = website_handler.get_short_url()
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
