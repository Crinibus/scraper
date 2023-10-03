import logging

import scraper.database as db


def clean_datapoints() -> None:
    print("Cleaning data...")
    logging.getLogger(__name__).info("Cleaning database datapoints")

    all_products = db.get_all_products()
    datapoints_to_delete = []

    for product in all_products:
        datapoints = db.get_datapoints_by_product_codes([product.product_code])

        datapoints.sort(key=lambda product: product.date)

        for index, datapoint in enumerate(datapoints):
            if index in (0, len(datapoints) - 1):
                continue

            previous_datapoint = datapoints[index - 1]
            next_datapoint = datapoints[index + 1]

            if datapoint.price == previous_datapoint.price and datapoint.price == next_datapoint.price:
                datapoints_to_delete.append(datapoint)

    db.delete_all(datapoints_to_delete)

    print("Done cleaning data")
