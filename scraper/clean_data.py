from scraper.filemanager import Filemanager


def clean_data() -> None:
    print("Cleaning data...")
    records_data = Filemanager.get_record_data()

    for category_info in records_data.values():
        for product_info in category_info.values():
            for website_info in product_info.values():
                datapoints = website_info["datapoints"]

                new_datapoints = []

                for index, datapoint in enumerate(datapoints):
                    if index in (0, len(datapoints) - 1):
                        new_datapoints.append(datapoint)
                        continue

                    # Skip unnecessary datapoints
                    if datapoint["price"] == datapoints[index - 1]["price"] and datapoint["price"] == datapoints[index + 1]["price"]:
                        continue

                    new_datapoints.append(datapoint)

                website_info["datapoints"] = new_datapoints

    Filemanager.save_record_data(records_data)
    print("Done cleaning data")
