import pathlib
import configparser
import pandas as pd
import json
import csv


class Filemanager:
    # root path of this repository
    root_path = pathlib.Path(__file__).parent.parent.absolute()

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
        data = Filemanager.read_json(f"{Filemanager.root_path}/scraper/records.json")
        return data

    @staticmethod
    def save_record_data(data: dict) -> None:
        Filemanager.write_json(f"{Filemanager.root_path}/scraper/records.json", data)

    @staticmethod
    def get_products_data() -> pd.DataFrame:
        df = pd.read_csv(
            f"{Filemanager.root_path}/scraper/products.csv", sep=",", header=0
        )
        return df

    @staticmethod
    def add_product_to_csv(category: str, url: str) -> None:
        data = [category, url]
        Filemanager.append_csv(f"{Filemanager.root_path}/scraper/products.csv", data)

    @staticmethod
    def clear_product_csv():
        Filemanager.clear_csv(f"{Filemanager.root_path}/scraper/products.csv")
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
        config = Config.read(f"{Filemanager.root_path}/scraper/settings.ini")
        return config["ChangeName"]

    @staticmethod
    def get_key_values(elements: list):
        for elem in elements:
            if "key" in elem:
                yield elem
