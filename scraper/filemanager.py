import pathlib
import configparser
from typing import Generator
import pandas as pd
import json
import csv


class Filemanager:
    # root path of this repository
    root_path = pathlib.Path(__file__).parent.parent.absolute()
    products_json_path = f"{root_path}/scraper/records.json"
    products_csv_path = f"{root_path}/scraper/products.csv"
    settings_ini_path = f"{root_path}/scraper/settings.ini"
    logging_ini_path = f"{root_path}/scraper/logging.ini"
    logfile_path = f"{root_path}/scraper/logfile.log"

    @staticmethod
    def read_json(filename: str) -> dict:
        with open(filename, "r", encoding="utf8") as file:
            data = json.load(file)
        return data

    @staticmethod
    def write_json(filename: str, data: dict):
        with open(filename, "w", encoding="utf8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    @staticmethod
    def append_csv(filename: str, data: list):
        with open(filename, "a", encoding="utf8", newline="") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(data)

    @staticmethod
    def clear_csv(filename: str):
        with open(filename, "w", encoding="utf8") as file:
            file.truncate()

    @staticmethod
    def get_record_data() -> dict:
        data = Filemanager.read_json(Filemanager.products_json_path)
        return data

    @staticmethod
    def save_record_data(data: dict) -> None:
        Filemanager.write_json(Filemanager.products_json_path, data)

    @staticmethod
    def get_products_data() -> pd.DataFrame:
        df = pd.read_csv(Filemanager.products_csv_path, sep=",", header=0)
        return df

    @staticmethod
    def add_product_to_csv(category: str, url: str) -> None:
        data = [category, url]
        Filemanager.append_csv(Filemanager.products_csv_path, data)

    @staticmethod
    def clear_product_csv() -> None:
        Filemanager.clear_csv(Filemanager.products_csv_path)
        # header for csv to use in pandas.DataFrame
        Filemanager.add_product_to_csv("category", "url")


class Config:
    @staticmethod
    def read(filename: str) -> configparser.ConfigParser:
        config = configparser.ConfigParser()
        config.read(filename)
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
    def get_key_values(elements: list) -> Generator[str, None, None]:
        for elem in elements:
            if "key" in elem:
                yield elem

    @staticmethod
    def get_request_delay() -> int:
        config = Config.read(Filemanager.settings_ini_path)
        return int(config["Scraping"]["request_delay"])
