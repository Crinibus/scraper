from typing import Iterator
import pathlib
import configparser


class Filemanager:
    # root path of this repository
    root_path = pathlib.Path(__file__).parent.parent.absolute()
    products_json_path = f"{root_path}/scraper/records.json"
    products_csv_path = f"{root_path}/scraper/products.csv"
    settings_ini_path = f"{root_path}/scraper/settings.ini"
    logging_ini_path = f"{root_path}/scraper/logging.ini"
    logfile_path = f"{root_path}/scraper/logfile.log"


class Config:
    @staticmethod
    def read(filename: str) -> configparser.ConfigParser:
        config = configparser.ConfigParser()
        config.read(filename, encoding="utf8")
        return config

    @staticmethod
    def write(filename: str, config: configparser.ConfigParser) -> None:
        with open(filename, "w") as default_file:
            config.write(default_file)

    @staticmethod
    def get_user_product_names() -> configparser.SectionProxy:
        """Get section 'ChangeName' from settings.ini file"""
        config = Config.read(Filemanager.settings_ini_path)
        return config["ChangeName"]

    @staticmethod
    def get_key_values(elements: list) -> Iterator[str]:
        for elem in elements:
            if "key" in elem:
                yield elem

    @staticmethod
    def get_request_delay() -> int:
        config = Config.read(Filemanager.settings_ini_path)
        return int(config["Scraping"]["request_delay"])

    @staticmethod
    def get_request_timeout() -> float | None:
        """Get request timeout - if number return float else return None"""
        config = Config.read(Filemanager.settings_ini_path)
        timeout = config["Scraping"]["request_timeout"]
        try:
            return float(timeout)
        except ValueError:
            return None
