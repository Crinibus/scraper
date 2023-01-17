from scraper.visualize import Product, MasterProduct, Datapoint, is_datapoints_up_to_date


def get_master_products(records_data: dict) -> tuple[MasterProduct]:
    master_products: list[MasterProduct] = []

    for category_name, category_info in records_data.items():
        for product_name, product_info in category_info.items():
            master_product = MasterProduct(product_name, category_name)
            for website_name, website_info in product_info.items():
                id = website_info["info"]["id"]
                url = website_info["info"]["url"]
                currency = website_info["info"]["currency"]
                datapoints = [Datapoint(datapoint["date"], datapoint["price"]) for datapoint in website_info["datapoints"]]
                is_up_to_date = is_datapoints_up_to_date(datapoints)
                product = Product(product_name, category_name, url, id, currency, website_name, datapoints, is_up_to_date)
                master_product.products.append(product)
            master_products.append(master_product)

    return tuple(master_products)

