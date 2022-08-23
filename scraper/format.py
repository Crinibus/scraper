from dataclasses import dataclass
from scraper.filemanager import Config, Filemanager


@dataclass
class Info:
    """Scraped info about product"""

    name: str
    price: float
    currency: str
    id: str
    valid: bool = True


class Format:
    @staticmethod
    def get_user_product_name(product_name: str) -> str:
        user_product_names = Config.get_user_product_names()

        for key in Config.get_key_values(user_product_names):
            key_list = user_product_names[key].split(",")
            value_key = f'value{key.strip("key")}'
            if all(elem in product_name for elem in key_list):
                return user_product_names[value_key]

        return product_name

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
