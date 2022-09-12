from typing import Generator, List, Tuple

from scraper.filemanager import Filemanager


def print_latest_datapoints(names: List[str], ids: List[str]):
    records_data = Filemanager.get_record_data()

    if names:
        print("\n----- SHOWING LATEST DATAPOINT FOR NAME(s) -----")
        for name in names:
            print(name.upper())
            # iterate the different websites the product with the specified name is scraped from
            for website_name, website_dict in get_product_info_with_name(name, records_data):
                print_latest_datapoint_with_name(website_name, website_dict)
            print()

    if ids:
        print("\n----- SHOWING LATEST DATAPOINT FOR ID(s) -----")
        for id in ids:
            product_name, website_name, website_dict = get_product_info_with_id(id, records_data)
            print_latest_datapoint_with_id(product_name, website_name, website_dict)


def get_product_info_with_name(name: str, records_data: dict) -> Generator[Tuple[str, str, dict], None, None]:
    for category_dict in records_data.values():
        for product_name, product_dict in category_dict.items():
            if not product_name.lower() == name.lower():
                continue
            for website_name, website_dict in product_dict.items():
                yield website_name, website_dict


def get_product_info_with_id(id: str, records_data: dict) -> Tuple[str, str, dict]:
    for category_dict in records_data.values():
        for product_name, product_dict in category_dict.items():
            for website_name, website_dict in product_dict.items():
                if website_dict["info"]["id"] == id:
                    return product_name, website_name, website_dict


def print_latest_datapoint_with_id(product_name: str, website_name: str, website_dict: dict):
    id = website_dict["info"]["id"]
    currency = website_dict["info"]["currency"]
    latest_datapoint = website_dict["datapoints"][-1]
    date = latest_datapoint["date"]
    price = latest_datapoint["price"]
    print(f"{product_name.upper()} - {id}")
    print(f"- {website_name.capitalize()}\n- {currency} {price}\n- {date}\n")


def print_latest_datapoint_with_name(website_name: str, website_dict: dict):
    id = website_dict["info"]["id"]
    currency = website_dict["info"]["currency"]
    latest_datapoint = website_dict["datapoints"][-1]
    date = latest_datapoint["date"]
    price = latest_datapoint["price"]
    print(f"> {website_name.capitalize()} - {id}\n  - {currency} {price}\n  - {date}")
