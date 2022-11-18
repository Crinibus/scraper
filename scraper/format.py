from dataclasses import dataclass
from scraper.filemanager import Config


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
