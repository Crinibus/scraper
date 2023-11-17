import time
from typing import Iterable
from sqlmodel import Session, select
from dataclasses import dataclass
import pandas as pd
import json

from scraper.filemanager import Config, Filemanager
from scraper.domains import get_website_handler
from scraper.models.product import DataPointInfo, MasterProduct, ProductInfo
from scraper.database.models import Product, DataPoint
from scraper.database.db import engine, create_db_and_tables


@dataclass
class ProductCSV:
    url: str
    short_url: str
    category: str


class FilemanagerLegacy:
    @staticmethod
    def read_json(filename: str) -> dict:
        with open(filename, "r", encoding="utf8") as file:
            data = json.load(file)
        return data

    @staticmethod
    def get_record_data() -> dict:
        data = FilemanagerLegacy.read_json(Filemanager.products_json_path)
        return data

    @staticmethod
    def save_record_data(data: dict) -> None:
        FilemanagerLegacy.write_json(Filemanager.products_json_path, data)

    @staticmethod
    def get_products_data() -> pd.DataFrame:
        df = pd.read_csv(Filemanager.products_csv_path, sep=",", header=0)
        return df

    @staticmethod
    def save_products_data(data_df: pd.DataFrame) -> None:
        data_df.to_csv(Filemanager.products_csv_path, sep=",", header=True, index=False)


class Format:
    @staticmethod
    def format_old_records_to_new() -> None:
        """Format records data from pre v1.1 to new records data format in v1.1"""
        records_data = FilemanagerLegacy.get_record_data()

        for category_info in records_data.values():
            for product_info in category_info.values():
                for website_info in product_info.values():
                    website_info["info"].update({"currency": "TBD"})
                    website_info.update({"datapoints": []})

                    for date_name, date_info in website_info["dates"].items():
                        website_info["datapoints"].append({"date": date_name, "price": float(date_info["price"])})

                    website_info.pop("dates")

        FilemanagerLegacy.save_record_data(records_data)

    @staticmethod
    def add_short_urls_to_products_csv() -> None:
        """Format products.csv to have short_url column - introduced in v2.3.0"""
        request_delay = Config.get_request_delay()

        products_df = FilemanagerLegacy.get_products_data()

        short_urls = []
        for _, row in products_df.iterrows():
            time.sleep(request_delay)
            website_handler = get_website_handler(row["url"])
            short_url = website_handler.get_short_url()

            # scrape only if short_url can't be created without
            if short_url is None:
                website_handler.get_product_info()
                short_url = website_handler.get_short_url()
            short_urls.append(short_url)

        products_df = products_df.drop("short_url", axis=1)
        products_df.insert(2, "short_url", short_urls, True)

        FilemanagerLegacy.save_products_data(products_df)

    @staticmethod
    def from_json_to_db() -> None:
        """Take the data in records.json and insert it in database - introduced in v3.0.0
        - NOTE all products in database will be deleted before inserting data from records.json"""

        create_db_and_tables()
        records = FilemanagerLegacy.get_record_data()
        products_df = FilemanagerLegacy.get_products_data()

        products_from_csv = [
            ProductCSV(category=category, url=url, short_url=short_url)
            for category, url, short_url in zip(products_df["category"], products_df["url"], products_df["short_url"])
        ]

        master_products = get_master_products(records)
        products_from_json = get_products_from_master_products(master_products)

        products_to_db: list[Product] = []
        for product_json in products_from_json:
            product_to_db = Product(
                name=product_json.product_name,
                product_code=product_json.id,
                domain=product_json.website,
                url="",
                short_url=product_json.url,
                category=product_json.category,
                is_active=False,
            )

            for product_csv in products_from_csv:
                if product_csv.short_url == product_json.url:
                    product_to_db.url = product_csv.url
                    product_to_db.is_active = True

            products_to_db.append(product_to_db)

        datapoints_to_db: list[DataPoint] = []
        for product in products_from_json:
            for datapoint in product.datapoints:
                datapoint_to_db = DataPoint(
                    product_code=product.id, date=datapoint.date, price=datapoint.price, currency=product.currency
                )
                datapoints_to_db.append(datapoint_to_db)

        with Session(engine) as session:
            products_in_db = session.exec(select(Product)).all()
            for product_in_db in products_in_db:
                session.delete(product_in_db)

            datapoints_in_db = session.exec(select(DataPoint)).all()
            for datapoint_in_db in datapoints_in_db:
                session.delete(datapoint_in_db)

            session.add_all(products_to_db)
            session.add_all(datapoints_to_db)

            session.commit()

        with Session(engine) as session:
            products_in_db = session.exec(select(Product)).all()
            datapoints_in_db = session.exec(select(DataPoint)).all()
            print(f"Inserted products to db: {len(products_in_db)}")
            print(f"Inserted datapoints to db: {len(datapoints_in_db)}")


def get_master_products(records_data: dict) -> tuple[MasterProduct]:
    master_products: list[MasterProduct] = []

    for category_name, category_info in records_data.items():
        for product_name, product_info in category_info.items():
            master_product = MasterProduct(product_name, category_name)
            for website_name, website_info in product_info.items():
                id = website_info["info"]["id"]
                url = website_info["info"]["url"]
                currency = website_info["info"]["currency"]
                datapoints = [DataPointInfo(datapoint["date"], datapoint["price"]) for datapoint in website_info["datapoints"]]
                product = ProductInfo(product_name, category_name, url, id, currency, website_name, datapoints)
                master_product.products.append(product)
            master_products.append(master_product)

    return tuple(master_products)


def get_products_from_master_products(master_products: Iterable[MasterProduct]) -> list[ProductInfo]:
    return [product for master_product in master_products for product in master_product.products]
