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
            if short_url is None:
                website_handler.get_product_info()
                short_url = website_handler.get_short_url()
            short_urls.append(short_url)

        products_df = products_df.drop("short_url", axis=1)
        products_df.insert(2, "short_url", short_urls, True)

        Filemanager.save_products_data(products_df)
