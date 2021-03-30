import pathlib
# from configparser import ConfigParser, SectionProxy
import configparser
import logging
import json


class Filemanager:
    @staticmethod
    def get_root_path() -> str:
        """Return root path of this repository"""
        return pathlib.Path().parent.absolute()

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
    def get_record_data() -> dict:
        data = Filemanager.read_json(f"{Filemanager.get_root_path()}/scraper/records.json")
        return data

    @staticmethod
    def save_record_data(data: dict) -> None:
        Filemanager.write_json(f"{Filemanager.get_root_path()}/scraper/records.json", data)


class Config:
    @staticmethod
    def read(filename: str) -> configparser.ConfigParser:
        config = configparser.ConfigParser()
        config.read(filename)
        return config

    @staticmethod
    def write(filename: str, config: configparser.ConfigParser) -> None:
        with open(filename, 'w') as default_file:
            config.write(default_file)

    @staticmethod
    def get_user_product_names() -> configparser.SectionProxy:
        """Get section 'ChangeName' from settings.ini file"""
        config = Config.read(f"{Filemanager.get_root_path()}/scraper/settings.ini")
        return config['ChangeName']


class Logger:
    @staticmethod
    def create_logger(logger_name: str) -> logging:
        """Setup and return logger."""
        # Gets or creates a logger
        logger = logging.getLogger(logger_name)

        # Check if logger already has a handler
        if logger.hasHandlers():
            logger.handlers.clear()

        # set log level (lowest level)
        logger.setLevel(logging.DEBUG)

        # define file handler and set formatter
        file_handler = logging.FileHandler(f'{Filemanager.get_root_path()}/scraper/logfile.log')
        formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
        file_handler.setFormatter(formatter)

        # add file handler to logger
        logger.addHandler(file_handler)
        return logger

    @staticmethod
    def get_logger(logger_name: str) -> logging:
        return logging.getLogger(logger_name)
