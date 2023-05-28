from fastapi import FastAPI, Query
from pydantic import BaseModel
from scraper import Filemanager, Scraper
from scraper.visualize import (
    get_master_products,
    get_products_with_ids,
    get_products_from_master_products,
    get_master_products_with_categories,
    Product,
)

app = FastAPI()


@app.get("/records")
async def get_records(only_up_to_date: bool = False):
    records_data = Filemanager.get_record_data()
    master_products = get_master_products(records_data)
    products = get_products_from_master_products(master_products)

    if only_up_to_date:
        products = [product for product in products if product.is_up_to_date]

    ids = [product.id for product in products]
    return ids


@app.get("/products")
async def get_products(ids: list[str] = Query(default=[]), utd: bool = False):
    records_data = Filemanager.get_record_data()
    master_products = get_master_products(records_data)
    products = get_products_with_ids(master_products, ids, utd)
    return products


class ScrapeId(BaseModel):
    ids: list[str] | None = None
    categories: list[str] | None = None
    # TODO - add option to only scrape products from one or more websites, e.g. "komplett" and "proshop"
    only_up_to_date: bool = False


@app.post("/scrape")
async def scrape_ids(body: ScrapeId):
    records_data = Filemanager.get_record_data()
    master_products = get_master_products(records_data)

    products_to_scrape: list[Product] = []

    if body.ids:
        products_with_ids = list(get_products_with_ids(master_products, body.ids, body.only_up_to_date))
        products_to_scrape.extend(products_with_ids)

    if body.categories:
        master_products_with_categories = get_master_products_with_categories(
            master_products, body.categories, body.only_up_to_date
        )
        products_with_categories = get_products_from_master_products(master_products_with_categories)
        products_to_scrape.extend(products_with_categories)

    for product in products_to_scrape:
        s = Scraper(product.category, product.url)
        s.scrape_info()

    return "Scraped"
