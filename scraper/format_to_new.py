import time
from sqlmodel import Session, select

from scraper import Scraper
from scraper.filemanager import Config, Filemanager
from scraper.domains import get_website_handler
from scraper.visualize import get_master_products, get_products_from_master_products
from scraper.database.models import Product, DataPoint
from scraper.database.db import engine, create_db_and_tables


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

    @staticmethod
    def add_short_urls_to_products_csv() -> None:
        """Format products.csv to have short_url column - introduced in v2.3.0"""
        request_delay = Config.get_request_delay()

        products_df = Filemanager.get_products_data()

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

        Filemanager.save_products_data(products_df)

    @staticmethod
    def from_json_to_db() -> None:
        """Take the data in records.json and insert it in database - introduced in v3.0.0
        - NOTE all products in database will be deleted before inserting data from records.json"""

        create_db_and_tables()
        records = Filemanager.get_record_data()
        products_df = Filemanager.get_products_data()

        products_from_csv = [
            Scraper(category, short_url) for category, short_url in zip(products_df["category"], products_df["short_url"])
        ]

        master_products = get_master_products(records)
        products_from_json = get_products_from_master_products(master_products)

        products_to_db = [
            Product(
                name=product_from_json.product_name,
                productId=product_from_json.id,
                domain=product_from_json.website,
                url=product_from_json.url,
                isActive=any([product_from_json.url == product_from_csv.url for product_from_csv in products_from_csv]),
            )
            for product_from_json in products_from_json
        ]

        datapoints_to_db = []
        for product in products_from_json:
            for datapoint in product.datapoints:
                datapoint_to_db = DataPoint(
                    productId=product.id, date=datapoint.date, price=datapoint.price, currency=product.currency
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
