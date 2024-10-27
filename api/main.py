from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from scraper import Scraper
from scraper.format import Format
import scraper.database as db
from scraper.models import Info

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/product-codes")
async def get_ids(only_up_to_date: bool = False) -> list[str]:
    products = db.get_all_products(select_only_active=only_up_to_date)

    ids = [product.product_code for product in products]
    return ids


@app.get("/products")
async def get_products(pcode: list[str] = Query(default=[]), with_datapoints: bool = False):
    if with_datapoints:
        products_db = db.get_products_by_product_codes(pcode)
        products = db.get_product_infos_from_products(products_db)
    else:
        products = db.get_products_by_product_codes(pcode)

    return products


@app.get("/products/all")
async def get_all_products(only_up_to_date: bool = False):
    products_db = db.get_all_products(select_only_active=only_up_to_date)
    products = Format.db_products_to_product_infos(products_db)

    return products


@app.get("/scrape/ids")
async def scrape_ids(ids: list[str] = Query(default=[])) -> list[Info]:
    products_to_scrape = db.get_products_by_product_codes(ids)

    scraped_infos = []

    for product in products_to_scrape:
        s = Scraper(product.category, product.url)
        scraped_info = s.scrape_info()
        scraped_infos.append(scraped_info)

    return scraped_infos
