import logging
from scraper import Filemanager


def reset():
    print("Resetting data...")
    logging.getLogger(__name__).info("Resetting data")

    data = Filemanager.get_record_data()

    for category in data.values():
        for product in category.values():
            for website in product.values():
                website["info"] = {"id": "", "url": "", "currency": ""}
                website["datapoints"] = []

    Filemanager.save_record_data(data)


def hard_reset():
    print("Hard resetting data...")
    logging.getLogger(__name__).info("Hard resetting data")

    data = {}
    Filemanager.save_record_data(data)
    Filemanager.clear_product_csv()
