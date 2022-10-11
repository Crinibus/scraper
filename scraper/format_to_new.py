import time

from scraper.filemanager import Config, Filemanager
from scraper.domains import get_website_handler


class Format:
    @staticmethod
    def format_old_records_to_new() -> None:
        """Format records data from pre v1.1 to new records data format in v1.1"""
        records_data = Filemanager.get_record_data()

        for category_info in records_data.values():
            for product_info in category_info.values():
                for website_info in product_info.values():
                    website_info["info"].update({"currency": "TBD"})
                    website_info.update({"datapoints": []})

                    for date_name, date_info in website_info["dates"].items():
                        website_info["datapoints"].append({"date": date_name, "price": float(date_info["price"])})

                    website_info.pop("dates")

        Filemanager.save_record_data(records_data)
