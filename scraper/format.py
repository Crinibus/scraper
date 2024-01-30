import scraper.database as db
from scraper.models.product import ProductInfo
from scraper.scrape import Scraper
from scraper.domains import get_website_name


class Format:
    def db_products_to_scrapers(products: list[db.Product]) -> list[Scraper]:
        scrapers = []
        for product in products:
            scraper = Format.db_product_to_scraper(product)
            scrapers.append(scraper)
        return scrapers

    @staticmethod
    def db_product_to_scraper(product: db.Product) -> Scraper:
        return Scraper(category=product.category, url=product.short_url)

    @staticmethod
    def scraper_to_db_product(product: Scraper, is_active: bool) -> db.Product:
        return db.Product(
            product_code=product.product_info.id,
            name=product.product_info.name,
            category=product.category,
            domain=product.website_handler.website_name,
            url=product.url,
            short_url=product.website_handler.get_short_url(),
            is_active=is_active,
        )

    @staticmethod
    def db_products_to_product_infos(products: list[db.Product]) -> list[ProductInfo]:
        product_infos = []
        for product in products:
            product_info = Format.db_product_to_product_info(product)
            product_infos.append(product_info)
        return product_infos

    @staticmethod
    def db_product_to_product_info(product: db.Product) -> ProductInfo:
        return ProductInfo(
            product_name=product.name,
            category=product.category,
            url=product.short_url,
            id=product.product_code,
            currency=None,
            website=get_website_name(product.short_url, keep_subdomain=False),
            datapoints=None,
        )
